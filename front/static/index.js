// const port = 8000;
const port = 48000;


const createAndInsertComponent = (elementType, elementBody, elementClasses, errorBody) => {
    let element = document.createElement(elementType);
    element.classList = elementClasses || [];
    element.innerHTML = elementBody;

    let error = document.createElement('span');
    error.classList = ['error-span'];
    error.setAttribute('id', 'error');
    error.innerHTML = errorBody || '';

    document.body.innerHTML = '';

    document.body.appendChild(element);
    document.body.appendChild(error);
}

const controlPanelElement = ( 
    `<div class="control-panel">
        <button type="button" onclick="createEnterElement()">Вход</button>
        <button type="button" onclick="createRegistrationElement()">Регистрация</button>
        <button type="button" onclick="authorization()">Авторизация</button>
    </div>`
);

const createRegistrationElement = () => {
    const elementBody = 
    `${controlPanelElement}
    <h2>Форма регистрации</h2>
        <form id="loginForm">
            <label for="username">Логин:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password"><br><br>
            <label for="password2">Пароль2:</label>
            <input type="password" id="password2" name="password"><br><br>
            <button type="button" onclick="registration()">Регистрация</button>
        </form>`;

    createAndInsertComponent('div', elementBody);
}

const createEnterElement = () => {
    const elementBody = 
    `${controlPanelElement}
    <h2>Форма логина</h2>
        <form id="loginForm">
            <label for="username">Логин:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password"><br><br>

            <button type="button" onclick="authentication()">Войти</button>
        </form>`;

    createAndInsertComponent('div', elementBody);
}

const createAuthorizeElement = () => {
    const elementBody = `
    <button type="button" onclick="logOut()">Выйти</button>
    <span>Авторизован</span>
    
    `;
    createAndInsertComponent('div', elementBody);
}


const setError = (message) => {
    let error = document.getElementById('error');
    if (error)
        error.innerHTML = message || '';
}

const registration = () => {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value;

    if (password !== password2) {
        setError('Пароли не совпадают');
        return;
    }

    var data = {
        username: username,
        password: password
    };

    postRequest(`http://localhost:${port}/registration`, data, createAuthorizeElement);
}

const authentication = () => {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    var data = {
        username: username,
        password: password
    };

    postRequest(`http://localhost:${port}/authentication`, data, createAuthorizeElement);
}

const authorization = (successFunc = null, failureFunc = null) => {
    postRequest(`http://localhost:${port}/authorization`, {}, successFunc, failureFunc);
}

const logOut = () => {
    postRequest(`http://localhost:${port}/log_out`, {}, startFunction);
}

const postRequest = (url, body, successFunc = null, failureFunc = null) => {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(errorMessage => {
                setError(JSON.parse(errorMessage)?.detail || '');
                console.log('false');
                failureFunc && failureFunc();
            });
          }
        console.log('true');
        successFunc && successFunc();
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

const startFunction = () => {
    authorization(createAuthorizeElement, createEnterElement);
}

window.onload = startFunction;
