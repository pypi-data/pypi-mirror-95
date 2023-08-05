/* Part of pythumbnailer: https://gitlab.com/somini/pythumbnailer/ */

currentMedia = null;

function activateMedia(media, simplify=true, new_history=false) {
	console.log(`Clicked on media`, media);

	var fullscreen = document.getElementById("fullscreen");
	var title = media.querySelector('.title').innerText;
	console.log('- Title:', title);
	var url = media.querySelector('a.photo').href;
	console.log('- URL:', url);

	fullscreen.querySelector('.title').innerText = title;
	var element_image = document.getElementById('fullscreen-picture-image');
	var element_video = document.getElementById('fullscreen-picture-video');
	element_image.classList.add("hidden");
	element_video.classList.add("hidden");
	var mime = media.dataset['mime'];
	if (mime.startsWith('image')) {
		element_image.src = url;
		element_image.classList.remove('hidden');
	}
	else if (mime.startsWith('video')) {
		var thumbnail = media.querySelector('img.photo').src;
		console.log('-- Thumbnail', thumbnail);
		element_video.src = url;
		// element_video.poster = thumbnail;
		element_video.classList.remove('hidden');
	}
	else {
		console.log(`Unsupported MIME Type: '${mime}'`);
	}

	if (simplify) {
		fullscreen.classList.remove("simple");  // Default to the complicated UI
	}
	fullscreen.classList.remove("hidden");  // Show fullscreen page

	currentMedia = media;
	if (new_history === true) {
		// Create a new history location
		window.location.hash = title;
	}
	else {
		// Replace the existing states
		history.replaceState(true, '', `#${title}`);
	}
}

function toggleMedia(e) {
	if (currentMedia == null) {
		var firstMedia = document.getElementById('album').firstElementChild;
		activateMedia(firstMedia);
	}
	else {
		closeFullscreen();
	}
}

function onPhotoClick(e) {
	event.preventDefault(); // Don't run the usual "click" stuff
	return activateMedia(this);
}

function onPhotoPrevious(e) {
	if (currentMedia != null) {
		var sibling = currentMedia.previousElementSibling;
		console.log("Previous Sibling:", sibling);
		if (sibling != null) {
			activateMedia(sibling, simplify=false);
		}
	}
}
function onPhotoNext(e) {
	if (currentMedia != null) {
		var sibling = currentMedia.nextElementSibling;
		console.log("Next Sibling:", sibling);
		if (sibling != null) {
			activateMedia(sibling, simplify=false);
		}
	}
}

function closeFullscreen(e) {
	console.log("Close the FullScreen media");
	document.getElementById('fullscreen').classList.add("hidden");

	currentMedia = null;
	history.replaceState(true, '', '#');  // Replace the URL with an empty title
}
function toggleUI(e) {
	var fullscreen = document.getElementById("fullscreen");
	console.log(`Simple UI: ${fullscreen.classList.contains("simple")}`);
	fullscreen.classList.toggle("simple");
}

function onKeybind(e) {
	if (e.code == 'Escape') {
		closeFullscreen();
	}
	else if (e.code == 'KeyF') {
		if (e.shiftKey == true) {
			toggleUI();
		}
		else {
			toggleMedia();
		}
	}
	else if (['ArrowLeft', 'KeyP'].includes(e.code)) {
		onPhotoPrevious();
	}
	else if (['ArrowRight', 'KeyN'].includes(e.code)) {
		onPhotoNext();
	}
	else {
		// No capture, keep going
		return true;
	}
	event.preventDefault(); // Don't run the usual stuff
	return false;
}


window.addEventListener('DOMContentLoaded', (event) => {
	console.log("Setup keybinds");
	document.addEventListener('keydown', onKeybind, false);

	console.log("Attaching events to helpers");
	var fullscreen = document.getElementById("fullscreen");
	document.getElementById('fullscreen-close')
		.addEventListener('click', closeFullscreen, false);
	document.getElementById('fullscreen-picture-image')
		.addEventListener('click', toggleUI, false);
	document.getElementById('fullscreen-previous')
		.addEventListener('click', onPhotoPrevious, false);
	document.getElementById('fullscreen-next')
		.addEventListener('click', onPhotoNext, false);

	var medias = document.querySelectorAll('li.photo');
	console.log(`Media Amount: ${medias.length}`)

	console.log('Attaching events to media');

	medias.forEach((media_li) => {
		media_li.addEventListener('click', onPhotoClick, false);
	});

	console.log('Attached all events');

	var hash_title = window.location.hash.substring(1)
	if (hash_title !== "") {
		var hash_media = null;
		for (let media_idx in medias) {
			media_li = medias[media_idx];
			// Search for the media with the given title
			if (media_li.querySelector('.title').innerText == hash_title) {
				hash_media = media_li;
				break;
			}
		}
		if (hash_media !== null) {
			console.log(`Select media with title: '${hash_title}'`);
			activateMedia(hash_media, new_history=true);
		}
		else {
			console.log('Unknown title');
		}
	}
});
