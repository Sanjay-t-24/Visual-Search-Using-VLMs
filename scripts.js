const uploadForm = document.getElementById('upload-form');
const imageInput = document.getElementById('image-input');
const previewDiv = document.getElementById('image-preview');
const resultDiv = document.getElementById('result');

imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            previewDiv.innerHTML = `<img src="${reader.result}" alt="Uploaded Image" style="max-width: 300px; margin-top: 10px;">`;
        };
        reader.readAsDataURL(file);
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = imageInput.files[0];
    if (!file) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to fetch result');
        }

        const data = await response.json();

        resultDiv.innerHTML = `
            <h3>Generated Description:</h3>
            <p>${data.description}</p>
        `;

        if (data.products.length > 0) {
            resultDiv.innerHTML += '<h3>Matching Products:</h3>';
            data.products.forEach(product => {
                resultDiv.innerHTML += `
                    <div>
                        <a href="${product.link}" target="_blank">${product.title}</a> - ${product.price} ${product.currency}
                    </div>
                `;
            });
        } else {
            resultDiv.innerHTML += '<p>No matching products found.</p>';
        }

    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = 'An error occurred while fetching the result.';
    }
});


