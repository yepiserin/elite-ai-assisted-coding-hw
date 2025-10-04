// MICE Card Form Handling
let editingMiceCardId = null;

function showMiceForm() {
    document.getElementById('mice-form').classList.remove('hidden');
    document.getElementById('add-mice-btn').classList.add('hidden');
}

function hideMiceForm() {
    document.getElementById('mice-form').classList.add('hidden');
    document.getElementById('add-mice-btn').classList.remove('hidden');
    document.getElementById('mice-card-form').reset();
    editingMiceCardId = null;
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

    const url = editingMiceCardId
        ? `/api/mice-cards/${editingMiceCardId}`
        : '/api/mice-cards';

    const method = editingMiceCardId ? 'PUT' : 'POST';

    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    });

    if (response.ok) {
        window.location.reload();
    }
}

function editMiceCard(id, code, opening, closing, nesting_level) {
    editingMiceCardId = id;
    document.getElementById('code').value = code;
    document.getElementById('opening').value = opening;
    document.getElementById('closing').value = closing;
    document.getElementById('nesting_level').value = nesting_level;
    showMiceForm();
}

async function deleteMiceCard(id) {
    const response = await fetch(`/api/mice-cards/${id}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        window.location.reload();
    }
}

// Try Card Form Handling
let editingTryCardId = null;

function showTryForm() {
    document.getElementById('try-form').classList.remove('hidden');
    document.getElementById('add-try-btn').classList.add('hidden');
}

function hideTryForm() {
    document.getElementById('try-form').classList.add('hidden');
    document.getElementById('add-try-btn').classList.remove('hidden');
    document.getElementById('try-card-form').reset();
    editingTryCardId = null;
}

async function submitTryCard(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        type: formData.get('type'),
        attempt: formData.get('attempt'),
        failure: formData.get('failure'),
        consequence: formData.get('consequence'),
        order_num: parseInt(formData.get('order_num'))
    };

    const url = editingTryCardId
        ? `/api/try-cards/${editingTryCardId}`
        : '/api/try-cards';

    const method = editingTryCardId ? 'PUT' : 'POST';

    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(data)
    });

    if (response.ok) {
        window.location.reload();
    }
}

function editTryCard(id, type, attempt, failure, consequence, order_num) {
    editingTryCardId = id;
    document.getElementById('type').value = type;
    document.getElementById('attempt').value = attempt;
    document.getElementById('failure').value = failure;
    document.getElementById('consequence').value = consequence;
    document.getElementById('order_num').value = order_num;
    showTryForm();
}

async function deleteTryCard(id) {
    const response = await fetch(`/api/try-cards/${id}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        window.location.reload();
    }
}

// Clear all data
async function clearAllData() {
    if (confirm('Are you sure you want to delete all cards? This cannot be undone.')) {
        const response = await fetch('/api/clear-data', {
            method: 'POST'
        });

        if (response.ok) {
            window.location.reload();
        }
    }
}

// Toggle theory panel
function toggleTheoryPanel() {
    const panel = document.getElementById('theory-panel');
    panel.classList.toggle('hidden');
}
