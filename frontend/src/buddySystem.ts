// frontend/src/api/buddySystem.ts

export async function initMemory(totalSize: number, unit: 'MB' | 'KB') {
    const res = await fetch('http://127.0.0.1:8000/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ total_size: totalSize, unit }),
    });
    return res.json();
}

export async function addProcess(process_id: string, process_size: number, unit: 'MB' | 'KB') {
    const res = await fetch('http://127.0.0.1:8000/add_process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process_id, process_size, unit }),
    });
    if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Error al agregar proceso');
    }
    return res.json();
}

export async function removeProcess(process_id: string) {
    const res = await fetch('http://127.0.0.1:8000/remove_process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process_id }),
    });
    return res.json();
}

export async function getTree() {
    const res = await fetch('http://127.0.0.1:8000/tree');
    return res.json();
}