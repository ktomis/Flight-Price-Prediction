const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);
const MIN_FLIGHT_DURATION = 30;
const ERROR_DISPLAY_DURATION = 5000;

class FlightBooking {
    constructor() {
        this.form = $('.container-form');
        this.loading = $('#loading');
        this.errorMessage = $('#error-message');
        this.btnClose = $('.prediction-price');
        this.submit = $('.submit-section');
        this.predictionSection = $('.prediction-section');
        
        this.initializeEventListeners();
        this.setMinimumDepartureDate();
    }

    initializeEventListeners() {

        if (this.btnClose && this.submit) {
            this.btnClose.addEventListener('click', () => this.btnClose.classList.add('active'));
            this.submit.addEventListener('click', () => this.btnClose.classList.remove('active'));
        }

        ['dep_date', 'arr_date'].forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.addEventListener('change', () => this.calculateDuration());
            }
        });

        ['source', 'destination'].forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.addEventListener('change', () => this.validateLocations());
            }
        });

        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                if (!this.validateForm()) {
                    e.preventDefault();
                }
            });
        }

        if (this.predictionSection) {
            const closeIcon = this.predictionSection.querySelector('.form-icon');
            if (closeIcon) {
                closeIcon.addEventListener('click', () => {
                    this.predictionSection.style.animation = 'close 1s forwards';
                    this.predictionSection.addEventListener('animationend', () => {
                        this.predictionSection.style.display = 'none';
                        this.btnClose.style.display = 'none';
                    });
                });
            }
        }
    }

    showError(message) {
        if (this.errorMessage) {
            this.errorMessage.textContent = message;
            this.errorMessage.style.display = 'block';
            this.errorMessage.style.color = '#eb4034';

            setTimeout(() => {
                this.errorMessage.style.display = 'none';
            }, ERROR_DISPLAY_DURATION);
        }
    }

    validateLocations() {
        const source = $('#source')?.value;
        const destination = $('#destination')?.value;

        if (source && destination && source === destination) {
            this.showError('Điểm đi và điểm đến không được trùng nhau');
            return false;
        }
        return true;
    }

    calculateDuration() {
        const depDate = new Date($('#dep_date')?.value);
        const arrDate = new Date($('#arr_date')?.value);
        
        if (!depDate || !arrDate) {
            $('#duration_display').textContent = "Vui lòng chọn ngày giờ";
            return false;
        }

        const minArrivalTime = new Date(depDate.getTime() + MIN_FLIGHT_DURATION * 60000);
        if (arrDate < minArrivalTime) {
            let durationDisplay = $('#duration_display');
            durationDisplay.style.color = "#eb4034";
            durationDisplay.textContent = `Thời gian đến phải sau thời gian đi ít nhất ${MIN_FLIGHT_DURATION} phút`;
            return false;
        }        

        const diffTime = Math.abs(arrDate - depDate);
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffTime % (1000 * 60 * 60)) / (1000 * 60));

        $('#duration_display').textContent = `${diffHours} giờ ${diffMinutes} phút`;
        $('#duration_hours').value = diffHours;
        $('#duration_minutes').value = diffMinutes;

        return true;
    }

    validateForm() {
        const depDate = new Date($('#dep_date')?.value);
        const arrDate = new Date($('#arr_date')?.value);

        if (!depDate || !arrDate) {
            this.showError('Vui lòng chọn ngày giờ bay');
            return false;
        }

        const minArrivalTime = new Date(depDate.getTime() + MIN_FLIGHT_DURATION * 60000);
        if (arrDate < minArrivalTime) {
            this.showError(`Thời gian đến phải sau thời gian đi ít nhất ${MIN_FLIGHT_DURATION} phút`);
            return false;
        }

        if (!this.validateLocations()) {
            return false;
        }

        if (!this.calculateDuration()) {
            return false;
        }

        const requiredFields = ['source', 'destination', 'airline', 'stopage', 'flight_class'];
        for (const field of requiredFields) {
            const element = $(`#${field}`);
            if (element && !element.value) {
                this.showError(`Vui lòng chọn ${element.previousElementSibling.textContent}`);
                return false;
            }
        }

        if (this.loading) {
            this.loading.style.display = 'block';
        }
        return true;
    }

    setMinimumDepartureDate() {
        const depDateInput = $('#dep_date');
        if (depDateInput) {
            const today = new Date();
            const minDate = today.toISOString().split('T')[0];
            depDateInput.setAttribute('min', minDate);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new FlightBooking();
});