// Configuration et données
const cities = {
    paris: {
        name: 'Paris',
        image: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500',
        description: 'La ville lumière'
    },
    lille: {
        name: 'Lille',
        image: 'https://images.unsplash.com/photo-1617803017416-3eb3b5d86f46?w=500',
        description: 'Capitale des Flandres'
    },
    lyon: {
        name: 'Lyon',
        image: 'https://images.unsplash.com/photo-1631857455684-a54a2f0473cd?w=500',
        description: 'Capitale de la gastronomie'
    },
    marseille: {
        name: 'Marseille',
        image: 'https://images.unsplash.com/photo-1589786722075-63d790383f6f?w=500',
        description: 'La cité phocéenne'
    }
};

// État global
let stepCount = 2; // Commence à 2 car nous avons déjà l'étape de départ (1)
let isDragging = false;
let currentDrag = null;

// Gestionnaire principal du formulaire de roadtrip
class RoadtripManager {
    constructor() {
        this.form = document.getElementById('roadtripForm');
        this.stepsContainer = document.getElementById('stepsContainer');
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Écouter les changements de ville
        this.stepsContainer.addEventListener('change', (e) => {
            if (e.target.classList.contains('city-select')) {
                this.updateCityPreview(e.target);
            }
        });

        // Validation du formulaire
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.validateAndSubmit();
        });
    }

    // Ajout d'une nouvelle étape
    addStep() {
        stepCount++;
        const newStep = this.createStepElement(stepCount);
        this.stepsContainer.appendChild(newStep);
        this.initializeDragAndDrop(newStep);

        // Animation d'entrée
        newStep.style.opacity = '0';
        newStep.style.transform = 'translateY(20px)';
        requestAnimationFrame(() => {
            newStep.style.opacity = '1';
            newStep.style.transform = 'translateY(0)';
        });
    }

    // Création d'un élément d'étape
    createStepElement(number) {
        const stepGroup = document.createElement('div');
        stepGroup.className = 'step-group';
        stepGroup.setAttribute('data-step', number);
        stepGroup.draggable = true;

        stepGroup.innerHTML = `
            <div class="step-number">${number}</div>
            <div class="step-content">
                <div class="form-group">
                    <label>Étape ${number}</label>
                    <select name="step_${number}" required class="city-select">
                        <option value="" selected disabled>Choisir une ville</option>
                        ${this.generateCityOptions()}
                    </select>
                    <div class="city-preview">
                        <div class="city-info">
                            <h3>Sélectionnez une ville</h3>
                            <p>Choisissez votre prochaine destination</p>
                        </div>
                    </div>
                </div>
            </div>
            <button type="button" class="btn-remove-step" onclick="roadtripManager.removeStep(this)" title="Supprimer cette étape">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
                    <path d="M6 18L18 6M6 6l12 12" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        `;

        return stepGroup;
    }

    // Génération des options de ville
    generateCityOptions() {
        return Object.entries(cities)
            .map(([value, { name }]) => `<option value="${value}">${name}</option>`)
            .join('');
    }

    // Mise à jour de l'aperçu de la ville
    updateCityPreview(select) {
        const cityData = cities[select.value];
        const previewDiv = select.parentElement.querySelector('.city-preview');

        if (cityData) {
            previewDiv.style.backgroundImage = `url('${cityData.image}')`;
            previewDiv.innerHTML = `
                <div class="city-info">
                    <h3>${cityData.name}</h3>
                    <p>${cityData.description}</p>
                </div>
            `;
        }
    }

    // Suppression d'une étape
    removeStep(button) {
        const stepGroup = button.closest('.step-group');

        // Animation de sortie
        stepGroup.style.opacity = '0';
        stepGroup.style.transform = 'translateY(20px)';

        setTimeout(() => {
            stepGroup.remove();
            this.updateStepNumbers();
        }, 300);
    }

    // Mise à jour des numéros d'étapes
    updateStepNumbers() {
        const steps = this.stepsContainer.querySelectorAll('.step-group');
        steps.forEach((step, index) => {
            const number = index + 1;
            step.querySelector('.step-number').textContent = number;
            step.setAttribute('data-step', number);

            const select = step.querySelector('.city-select');
            select.name = `step_${number}`;

            const label = step.querySelector('label');
            if (number === 1) {
                label.textContent = 'Point de départ';
            } else {
                label.textContent = `Étape ${number}`;
            }
        });
        stepCount = steps.length;
    }

    // Initialisation du drag & drop
    initializeDragAndDrop(element) {
        element.addEventListener('dragstart', this.handleDragStart.bind(this));
        element.addEventListener('dragend', this.handleDragEnd.bind(this));
        element.addEventListener('dragover', this.handleDragOver.bind(this));
        element.addEventListener('drop', this.handleDrop.bind(this));
    }

    // Gestionnaires d'événements drag & drop
    handleDragStart(e) {
        isDragging = true;
        currentDrag = e.target;
        e.target.classList.add('dragging');
        e.dataTransfer.setData('text/plain', e.target.getAttribute('data-step'));
    }

    handleDragEnd(e) {
        isDragging = false;
        currentDrag = null;
        e.target.classList.remove('dragging');
    }

    handleDragOver(e) {
        e.preventDefault();
        if (!isDragging) return;

        const step = e.target.closest('.step-group');
        if (step && step !== currentDrag) {
            const rect = step.getBoundingClientRect();
            const midY = rect.top + rect.height / 2;

            if (e.clientY < midY) {
                step.parentNode.insertBefore(currentDrag, step);
            } else {
                step.parentNode.insertBefore(currentDrag, step.nextSibling);
            }

            this.updateStepNumbers();
        }
    }

    handleDrop(e) {
        e.preventDefault();
        this.updateStepNumbers();
    }

    // Validation et soumission du formulaire
    validateAndSubmit() {
        const formData = new FormData(this.form);
        const roadtrip = {
            name: formData.get('trip_name'),
            startDate: formData.get('start_date'),
            duration: formData.get('duration'),
            steps: []
        };

        // Collecte des étapes
        this.stepsContainer.querySelectorAll('.step-group').forEach(step => {
            const select = step.querySelector('.city-select');
            roadtrip.steps.push({
                order: parseInt(step.getAttribute('data-step')),
                city: select.value,
                cityName: select.options[select.selectedIndex].text
            });
        });

        // Validation
        if (roadtrip.steps.length < 2) {
            this.showError('Votre roadtrip doit contenir au moins 2 étapes');
            return;
        }

        if (new Set(roadtrip.steps.map(s => s.city)).size !== roadtrip.steps.length) {
            this.showError('Chaque ville ne peut être visitée qu\'une seule fois');
            return;
        }

        // Soumission (à implémenter selon vos besoins)
        console.log('Roadtrip à sauvegarder:', roadtrip);
        this.showSuccess('Votre roadtrip a été sauvegardé avec succès!');
    }

    // Gestion des notifications
    showError(message) {
        this.showNotification(message, 'error');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                ${message}
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">×</button>
        `;

        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }
}

// Initialisation
const roadtripManager = new RoadtripManager();

// Style pour les notifications
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    }

    .notification.error {
        background: #fee2e2;
        border-left: 4px solid #dc2626;
    }

    .notification.success {
        background: #dcfce7;
        border-left: 4px solid #16a34a;
    }

    .notification-close {
        background: none;
        border: none;
        font-size: 1.25rem;
        cursor: pointer;
        opacity: 0.5;
    }

    .notification-close:hover {
        opacity: 1;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .step-group.dragging {
        opacity: 0.5;
        cursor: move;
    }
`;

document.head.appendChild(style);