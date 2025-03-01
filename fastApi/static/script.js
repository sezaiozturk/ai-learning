const inputText = document.getElementById('inputText');
const resultDiv = document.getElementById('resultDiv');

const addText = ()=> {
    fetch('http://127.0.0.1:8000/addText', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: inputText.value
        })
      })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
}

const searchText = ()=> {
    fetch('http://127.0.0.1:8000/searchText', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: inputText.value
        })
      })
        .then(response => response.json())
        .then((data) => {
            if(data && data.length > 0) {
                resultDiv.innerHTML = '';
                data[0].forEach(item => {
                    const p = document.createElement('p');
                    p.textContent = item.text;
                    resultDiv.appendChild(p);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}