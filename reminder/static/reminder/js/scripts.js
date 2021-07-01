try {
    document.querySelector('#main').addEventListener('click', () => load_main());
    document.querySelector('#agendas').addEventListener('click', () => load_main());
    document.querySelector('#new').addEventListener('click', () => load_new());
    document.querySelector('#agenda-form').onsubmit = create_agenda;
    
    load_main()
} catch {

}

// HOME VIEW
function load_main() {
    document.querySelector('#main-view').style.display = 'block';
    document.querySelector('#new-view').style.display = 'none';
    document.querySelector('#agenda-view').style.display = 'none';
    document.querySelector('#day-view').style.display = 'none';

    fetch('/agendas')
    .then(response => response.json())
    .then(agendas => {
        
        if (agendas.length == 0) {
            let emptyCard = document.querySelector('#empty-card');
            let cards = document.querySelectorAll('#card');

            if (cards != null) {
                remove_agendas();
            }

            if (emptyCard == null) {
                let greatGrandParentDiv = document.createElement('div');
                let grandParentDiv = document.createElement('div');
                let fatherDiv = document.createElement('div');
                let childDiv = document.createElement('div');
                let mainView = document.querySelector('#main-view');

                greatGrandParentDiv.setAttribute('id', 'empty-card');

                greatGrandParentDiv.className = 'row row-cols-1 row-cols-md-4 g-4';
                grandParentDiv.className = 'col';
                fatherDiv.className = 'card text-white mb-3 empty-card pointer';
                childDiv.className = 'card-body mx-auto';

                childDiv.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-plus-lg" viewBox="0 0 16 16" style="color: grey;">
                        <path
                            d="M8 0a1 1 0 0 1 1 1v6h6a1 1 0 1 1 0 2H9v6a1 1 0 1 1-2 0V9H1a1 1 0 0 1 0-2h6V1a1 1 0 0 1 1-1z" />
                    </svg>
                `;

                fatherDiv.addEventListener('click', () => {
                    load_new();
                });

                fatherDiv.appendChild(childDiv);
                grandParentDiv.appendChild(fatherDiv);
                greatGrandParentDiv.appendChild(grandParentDiv);
                mainView.appendChild(greatGrandParentDiv);
            }
        } else if (agendas.length > 0) {
            let emptyCard = document.querySelector('#empty-card');
            let cards = document.querySelectorAll('#card');
            
            if (emptyCard != null) {
                emptyCard.remove();
            } else if (cards != null) {
                remove_agendas();
            }

            add_agendas(agendas);
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });

}

// CREATE CALENDAR VIEW
function load_new() {
    document.querySelector('#main-view').style.display = 'none';
    document.querySelector('#new-view').style.display = 'block';
    document.querySelector('#agenda-view').style.display = 'none';
    document.querySelector('#day-view').style.display = 'none';
    let title = document.querySelector('#agenda-title')

    title.value = '';
    document.querySelector('#agenda-description').value = '';

    title.className = 'input';

    let message = document.querySelector('#message');

    if (message != null) {
        message.remove();
    }
}

// CALENDAR VIEW
function load_agenda(agenda_id) {
    document.querySelector('#main-view').style.display = 'none';
    document.querySelector('#new-view').style.display = 'none';
    document.querySelector('#agenda-view').style.display = 'block';
    document.querySelector('#day-view').style.display = 'none';

    fetch(`/calendar/${agenda_id}`)
    .then(response => response.json())
    .then(cal => {
        let calendarDiv = document.querySelector('#calendar');
        calendarDiv.innerHTML = cal.calendar;

        let calendarTable = document.querySelector('.month');
        calendarTable.className += ' table table-bordered';
        calendarTable.style.tableLayout = 'fixed';

        let calendarTds = document.querySelectorAll('td');
        calendarTds.forEach(td => {
            let tdContent = td.innerHTML;
            tdContent = parseInt(td.innerHTML);
            if (tdContent < 10) {
                td.innerHTML = '0' + String(tdContent);
            }
            if (isNaN(tdContent) == false) {
                td.setAttribute('id', tdContent);
                
                if (td.id == cal.day) {
                    td.style.background = '#BBBBBB';

                    td.addEventListener('mouseover', () => {
                        td.style.backgroundColor = '#D3D3D3';
                    })
    
                    td.addEventListener('mouseout', () => {
                        td.style.backgroundColor = '#BBBBBB';
                    })
                } else {
                    td.addEventListener('mouseover', () => {
                        td.style.backgroundColor = '#D3D3D3';
                    })
    
                    td.addEventListener('mouseout', () => {
                        td.style.backgroundColor = '';
                    })
                }

                td.addEventListener('click', () => {
                    load_day(td.id, cal.month, cal.year, agenda_id);
                })
            }
            td.style.height = '90px';
            td.style.fontWeight = 'bold';
        })

        let calendarThs = document.querySelectorAll('th');
        let screenWidth = window.screen.width
        calendarThs.forEach(th => {
            if (th.className == 'month') {
                thContent = th.innerHTML.split(' ');
                if (thContent[0] == 'January') {
                    th.innerHTML = 'Janeiro ' + thContent[1];
                } else if (thContent[0] == 'February') {
                    th.innerHTML = 'Fevereiro ' + thContent[1];
                } else if (thContent[0] == 'March') {
                    th.innerHTML = 'Março ' + thContent[1];
                } else if (thContent[0] == 'April') {
                    th.innerHTML = 'Abril ' + thContent[1];
                } else if (thContent[0] == 'May') {
                    th.innerHTML = 'Maio ' + thContent[1];
                } else if (thContent[0] == 'June') {
                    th.innerHTML = 'Junho ' + thContent[1];
                } else if (thContent[0] == 'July') {
                    th.innerHTML = 'Julho ' + thContent[1];
                } else if (thContent[0] == 'August') {
                    th.innerHTML = 'Agosto ' + thContent[1];
                } else if (thContent[0] == 'September') {
                    th.innerHTML = 'Setembro ' + thContent[1];
                } else if (thContent[0] == 'October') {
                    th.innerHTML = 'Outubro ' + thContent[1];
                } else if (thContent[0] == 'November') {
                    th.innerHTML = 'Novembro ' + thContent[1];
                } else if (thContent[0] == 'December') {
                    th.innerHTML = 'Dezembro ' + thContent[1];
                }
            } else {
                if (screenWidth > 600) {
                    if (th.innerHTML == 'Sun') {
                        th.innerHTML = 'Domingo';
                    } else if (th.innerHTML == 'Mon') {
                        th.innerHTML = 'Segunda';
                    } else if (th.innerHTML == 'Tue') {
                        th.innerHTML = 'Terça';
                    } else if (th.innerHTML == 'Wed') {
                        th.innerHTML = 'Quarta';
                    } else if (th.innerHTML == 'Thu') {
                        th.innerHTML = 'Quinta';
                    } else if (th.innerHTML == 'Fri') {
                        th.innerHTML = 'Sexta';
                    } else if (th.innerHTML == 'Sat') {
                        th.innerHTML = 'Sábado';
                    }
                } else {
                    if (th.innerHTML == 'Sun') {
                        th.innerHTML = 'Dom';
                    } else if (th.innerHTML == 'Mon') {
                        th.innerHTML = 'Seg';
                    } else if (th.innerHTML == 'Tue') {
                        th.innerHTML = 'Ter';
                    } else if (th.innerHTML == 'Wed') {
                        th.innerHTML = 'Qua';
                    } else if (th.innerHTML == 'Thu') {
                        th.innerHTML = 'Qui';
                    } else if (th.innerHTML == 'Fri') {
                        th.innerHTML = 'Sex';
                    } else if (th.innerHTML == 'Sat') {
                        th.innerHTML = 'Sáb';
                    }
                }
            }
            th.classList.add('text-center');
        })
    })
    .catch(error => {
        console.log('Error:', error);
    })
}

// AGENDA VIEW
function load_day(day, month, year, agenda_id) {
    document.querySelector('#main-view').style.display = 'none';
    document.querySelector('#new-view').style.display = 'none';
    document.querySelector('#agenda-view').style.display = 'none';
    document.querySelector('#day-view').style.display = 'block';
    reminders = document.querySelectorAll('#reminder');
    inputReminders = document.querySelectorAll('#div-reminder');

    if (reminders.length > 0 || inputReminders.length > 0) {
        remove_reminders();
    }

    fetch(`/day/${day}/${month}/${year}/${agenda_id}`)
    .then(response => response.json())
    .then(data => {
        document.querySelector('#date').innerHTML = `${data[0].date}`;
        document.querySelector('#weekDay').innerHTML = `${data[0].weekDay}`;
        let content = data[0].content;
        if (content == undefined) {

        } else {
            for (i = 0; i < data.length; i++) {
                let li = document.createElement('li');
                let div = document.createElement('div');
                let button = document.createElement('button');
                li.id = 'reminder';
                li.dataset.key = `${i}`;
                li.className = 'list-group-item d-flex justify-content-between align-items-center pointer';
                div.innerHTML = `${data[i].content}`;
                button.className = 'btn shadow-none';
                button.innerHTML = 'x';
                button.addEventListener('click', () => {
                    fetch('/delete', {
                        method: 'POST',
                        body: JSON.stringify({
                            reminder: id
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(() => {
                        document.querySelector(`[data-key='${li.dataset.key}']`).remove();
                    })
                    .catch(error => {
                        console.log('Error:', error);
                    });
                })

                let id = data[i].reminder;

                if (data[i].scratched == true) {
                    div.style.textDecoration = 'line-through';
                    div.addEventListener('click', () => {
                        fetch(`/scratch/${id}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                scratched: false
                            }),
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                        .then(() => {
                            load_day(day, month, year, agenda_id);
                        })
                        .catch(error => {
                            console.log('Error:', error);
                        })
                    })
                } else {
                    div.addEventListener('click', () => {
                        fetch(`/scratch/${id}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                                scratched: true
                            }),
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                        .then(() => {
                            load_day(day, month, year, agenda_id);
                        })
                        .catch(error => {
                            console.log('Error:', error);
                        })
                    })
                }

                li.appendChild(div);
                li.appendChild(button);
                document.querySelector('#content').appendChild(li);
            }
        }
    })
    .then(() => {
        let li = document.createElement('li');
        let emptyLi = document.createElement('li');
        let input = document.createElement('input');
        let button = document.createElement('button');
        li.id = 'reminder';
        li.className = 'list-group-item d-flex justify-content-between align-items-center pointer';
        emptyLi.id = 'reminder';
        emptyLi.className = 'list-group-item d-flex justify-content-between align-items-center';
        input.type = 'text';
        input.id = 'new-reminder';
        input.className = 'form-control line-input shadow-none';
        button.type = 'submit';
        button.className = 'btn shadow-none reminder-button';
        button.innerHTML = '+';
        
        button.addEventListener('click', () => {
            const task = document.querySelector('#new-reminder').value;
            if (task == '') {

            } else {
                fetch('/create', {
                    method: 'POST',
                    body: JSON.stringify({
                        content: task,
                        agenda: agenda_id,
                        year: year,
                        month: month,
                        day: day
                    }),
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(() => {
                    load_day(day, month, year, agenda_id);
                })
                .catch(error => {
                    console.log('Error:', error);
                })
            }
        })
        
        li.appendChild(input);
        li.appendChild(button);
        document.querySelector('#content').appendChild(li);
        document.querySelector('#content').appendChild(emptyLi);
    })
    .catch(error => {
        console.log('Error:', error);
    })
}

// CREATE CALENDAR
function create_agenda() {
    const title = document.querySelector('#agenda-title').value;
    const description = document.querySelector('#agenda-description').value;
    const colorInput = document.querySelector('input[name="color"]')
    let color = '';

    try {
        color = document.querySelector('input[name="color"]:checked').value;
    } finally {
        if (title == '' || color == '') {
            let message = document.querySelector('#message');
            
            if (message == null) {
                let titleField = document.querySelector('#agenda-title');
                let colorField = colorInput.parentNode;
                let small = document.createElement('small');
    
                small.setAttribute('id', 'message');
    
                if (title == '' & color == '') {
                    titleField.className += ' border border-2 border-danger rounded';
                    colorInput.parentNode.className += ' border border-2 border-danger rounded';
                } else if (title == '') {
                    titleField.className += ' border border-2 border-danger rounded';
                } else {
                    colorInput.parentNode.className += ' border border-2 border-danger rounded';
                }

                small.className = 'text-muted';
    
                small.innerHTML = 'É necessário preencher todos os campos obrigatórios.';
    
                colorField.insertAdjacentElement("afterend", small);
            }
        } else {        
            fetch('/new', {
                method: 'POST',
                body: JSON.stringify({
                    title: title,
                    description: description,
                    color: color
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(() => {
                load_main()
            })
            .catch(error => {
                console.log('Error:', error);
            });
        }

        return false;
    }
}

// LOAD CALENDARS
function add_agendas(agendas) {
    let greatGrandParentDiv = document.createElement('div');
    let mainView = document.querySelector('#main-view');

    greatGrandParentDiv.setAttribute('id', 'card');

    greatGrandParentDiv.className = 'row row-cols-1 row-cols-md-4 g-4';

    agendas.forEach(agenda => {
        let grandParentDiv = document.createElement('div');
        let fatherDiv = document.createElement('div');
        let childDiv = document.createElement('div');
        let title = document.createElement('h5');
        let description = document.createElement('p');

        grandParentDiv.className = 'col';
        fatherDiv.className = `card text-white ${agenda.color} mb-3 pointer`;
        childDiv.className = 'card-body';
        title.className = 'card-title';
        description.className = 'card-text';

        title.innerHTML = agenda.title;
        description.innerHTML = agenda.description;

        fatherDiv.setAttribute('id', agenda.id);

        fatherDiv.addEventListener('click', () => {
            load_agenda(agenda.id);
        });

        childDiv.appendChild(title);
        childDiv.appendChild(description);
        fatherDiv.appendChild(childDiv);
        grandParentDiv.appendChild(fatherDiv);
        greatGrandParentDiv.appendChild(grandParentDiv);
        mainView.appendChild(greatGrandParentDiv);
    });
}

// HIDE CALENDARS
function remove_agendas() {
    const cards = document.querySelectorAll('#card');
    for (i = 0; i < cards.length; i++) {
        cards[i].remove();
    }
}

// HIDE REMINDERS
function remove_reminders() {
    const reminders = document.querySelectorAll('#reminder');
    const inputReminders = document.querySelectorAll('#div-reminder');
    for (i = 0; i < reminders.length; i++) {
        reminders[i].remove();
    }
    for (j = 0; j < inputReminders.length; j++) {
        inputReminders[j].remove();
    }
}

// GET COOKIE
function getCookie(key) {
    var cookies = document.cookie.split('; ');
    for (var i = 0, parts; (parts = cookies[i] && cookies[i].split('=')); i++) {
        if (decode(parts.shift()) === key) {
            return decode(parts.join('='));
        }
    }
    return null;
}

// DECODE
function decode(s) {
    return decodeURIComponent(s.replace(/\+/g, ' '));
}