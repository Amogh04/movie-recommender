const input = document.querySelector('form input');

const typed = ()=>{
	setTimeout(()=>{
		fetch('/', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ data: input.value })
		})
		.then(response => response.json())
		.then(data => {
			document.querySelector('.suggestion-item form input').value = data.suggestions;
			document.querySelector('.suggestion-item form button').innerText = data.suggestions;
			if(input.value!='')
				document.querySelector('.suggestion-item').classList.add('change-color');
			else
				document.querySelector('.suggestion-item').classList.remove('change-color');
		})
		.catch(error => console.error('Error:', error));
	},"50ms")
}
window.addEventListener("keydown",typed);
	