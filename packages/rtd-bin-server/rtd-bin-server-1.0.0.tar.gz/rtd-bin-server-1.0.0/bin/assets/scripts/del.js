function activateDeleteButton() {
	/* If the snippet have just been saved, the delete token
	   is found in the delTok cookie. We now have the corresponding
	   snippet id so we can link the two */
	const cookies = document.cookie.split('; ').filter(elt => {return elt.startsWith('delTok=')});
	if (cookies.length) {
		localStorage.setItem('delTok', cookies[0].substring(7));
	}

	/* If the snippet is found then this browser is the author and
	   we can show the delete button as we have the delete token */
	snippet.delTok = localStorage.getItem('delTok');
	if (snippet.delTok) {
		const btnDel = document.getElementById('controlButtonDelete');
		btnDel.setAttribute('href', `/del/${snippet.id}?token=${snippet.delTok}`);
		btnDel.removeAttribute('hidden');
	}
}

if (localStorage) {
	activateDeleteButton();
} else  {
	console.warning('The token deletion UI integration requires the local storage.');
}


