// Функция для отправки данных формы (например, для создания врача)
async function submitForm(event, formId, apiEndpoint, method = 'POST') {
    event.preventDefault(); // Предотвращаем перезагрузку страницы при отправке формы

    // Получаем данные формы
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    // Создаем объект с данными формы
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    // Отправляем данные на сервер
    try {
        const response = await fetch(apiEndpoint, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        // Обрабатываем ответ
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Ошибка при отправке данных:', error);
        alert('Произошла ошибка. Попробуйте снова.');
    }
}

// Пример: Привязываем форму для добавления врача
document.getElementById('doctor-form').addEventListener('submit', function(event) {
    submitForm(event, 'doctor-form', '/doctors');
});

// Функция для получения данных (например, список врачей)
async function fetchDoctors() {
    try {
        const response = await fetch('/doctors', { method: 'GET' });
        const doctors = await response.json();

        // Рендерим список врачей в HTML (например, в таблицу или список)
        const doctorList = document.getElementById('doctor-list');
        doctorList.innerHTML = ''; // Очищаем список перед добавлением новых элементов

        doctors.forEach(doctor => {
            const listItem = document.createElement('li');
            listItem.textContent = `${doctor.first_name} ${doctor.last_name} (Specialization ID: ${doctor.specialization_id})`;
            doctorList.appendChild(listItem);
        });

    } catch (error) {
        console.error('Ошибка при получении списка врачей:', error);
        alert('Не удалось загрузить список врачей.');
    }
}

// Пример: Получаем и выводим список врачей при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fetchDoctors();
});
