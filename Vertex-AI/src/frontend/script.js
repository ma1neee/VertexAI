const API_URL = "http://localhost:8000";

async function analyzeFile() {
    const fileInput = document.getElementById('pdfFile');

    if (fileInput.files.length === 0) {
        showError("Пожалуйста, выберите PDF файл");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/analyze/pdf/file`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);

    } catch (error) {
        showError(`Ошибка: ${error.message}`);
        console.error(error);
    } finally {
        document.getElementById('loader').classList.add('hidden');
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function renderResults(data) {
    const results = document.getElementById('results');
    results.classList.remove('hidden');

    const scoreEl = document.getElementById('scoreValue');
    const scoreLabel = document.getElementById('scoreLabel');
    const score = data.score;

    scoreEl.textContent = score !== null ? Math.round(score) : 'N/A';

    if (score !== null) {
        if (score >= 70) {
            scoreEl.style.background = 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
            scoreLabel.textContent = 'Отлично';
            scoreLabel.style.color = '#38ef7d';
        } else if (score >= 40) {
            scoreEl.style.background = 'linear-gradient(135deg, #f12711 0%, #f5af19 100%)';
            scoreLabel.textContent = 'Удовлетворительно';
            scoreLabel.style.color = '#f5af19';
        } else {
            scoreEl.style.background = 'linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%)';
            scoreLabel.textContent = 'Требует внимания';
            scoreLabel.style.color = '#ef473a';
        }
    }

    const metricsTable = document.querySelector('#metricsTable tbody');
    metricsTable.innerHTML = data.metrics.map(m => `
        <tr>
            <td>${m.name}</td>
            <td>${formatNumber(m.value)}</td>
            <td>${m.unit}</td>
            <td>${m.year || '-'}</td>
            <td>${Math.round(m.confidence_score * 100)}%</td>
        </tr>
    `).join('');

    const ratiosTable = document.querySelector('#ratiosTable tbody');
    ratiosTable.innerHTML = data.ratios.map(r => `
        <tr>
            <td>${r.name}</td>
            <td>${r.value !== null ? formatNumber(r.value) + ' ' + r.unit : 'N/A'}</td>
            <td><span class="category-badge">${r.category}</span></td>
        </tr>
    `).join('');

    document.getElementById('nlpSummary').textContent = data.nlp_summary || 'NLP анализ не доступен';

    const risksList = document.getElementById('risksList');
    risksList.innerHTML = data.risks.length > 0
        ? data.risks.map(r => `<li>${r}</li>`).join('')
        : '<li>Риски не выявлены</li>';

    const opportunitiesList = document.getElementById('opportunitiesList');
    opportunitiesList.innerHTML = data.opportunities.length > 0
        ? data.opportunities.map(o => `<li>${o}</li>`).join('')
        : '<li>Возможности не выявлены</li>';

    const recsList = document.getElementById('recsList');
    recsList.innerHTML = data.recommendations.map(r => `<li>${r}</li>`).join('');
}

function formatNumber(num) {
    if (num === null || num === undefined) return '-';
    if (typeof num === 'number') {
        if (Math.abs(num) >= 1000000) {
            return (num / 1000000).toFixed(2) + 'M';
        } else if (Math.abs(num) >= 1000) {
            return (num / 1000).toFixed(2) + 'K';
        }
        return num.toFixed(2);
    }
    return num;
}