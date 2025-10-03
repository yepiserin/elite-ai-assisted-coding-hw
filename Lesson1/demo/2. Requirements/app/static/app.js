// MICE Card Form Handling
function showMiceForm() {
    document.getElementById('mice-form').classList.remove('hidden');
    document.getElementById('add-mice-btn').classList.add('hidden');
}

function hideMiceForm() {
    document.getElementById('mice-form').classList.add('hidden');
    document.getElementById('add-mice-btn').classList.remove('hidden');
    document.getElementById('mice-card-form').reset();
}

async function submitMiceCard(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        code: formData.get('code'),
        opening: formData.get('opening'),
        closing: formData.get('closing'),
        nesting_level: parseInt(formData.get('nesting_level'))
    };

    const response = await fetch('/api/mice-cards', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    });

    if (response.ok) {
        window.location.reload();
    }
}
