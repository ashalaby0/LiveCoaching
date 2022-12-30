
// coach_stats
async function get_coach_stats() {
    const coach_stats_res = await fetch(coach_stats_url)
    let coach_stats_obj = await coach_stats_res.json()
    
    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    // let backgroundColorList =  Array.from({length:Object.values(coach_stats_obj).length},(v,k)=>((k+1)*15+0x000000).toString(16)).map(elem => `#55${elem}`);
    // draw chart
    let coachCtart = document.getElementById("coachChart").getContext('2d');
    let currentValH5 = document.querySelector("#currentNoOfCoaches")
    currentValH5.textContent = Object.values(coach_stats_obj).slice(-1)[0]
    new Chart(coachCtart, {
        type: 'bar',
        data: {
            labels: Object.keys(coach_stats_obj),
            datasets: [{
                label: '# of Coaches',
                data: Object.values(coach_stats_obj),
                backgroundColor: backgroundColorList,
            }]
        },
        options: {
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            },
            plugins: {
                tooltip: {
                    yAlign: 'bottom'
                }
            }
        }
    });
}
get_coach_stats()


// client stats
async function get_client_stats(){
    const client_stats_res = await fetch(client_stats_url)
    let client_status_obj = await client_stats_res.json()

    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    let currentValH5 = document.querySelector("#currentNoOfClients")
    currentValH5.textContent = Object.values(client_status_obj).slice(-1)[0]

    // let backgroundColorList =  Array.from({length:Object.values(client_status_obj).length},(v,k)=>((k+1)*15+0x000000).toString(16)).map(elem => `#55${elem}`);
    let clientCtart = document.getElementById("clientChart").getContext('2d');
    new Chart(clientCtart, {
        type: 'line',
        data: {
            labels: Object.keys(client_status_obj),
            datasets: [{
                label: '# of Clients',
                data: Object.values(client_status_obj),
                backgroundColor: '#ffb703',
                borderColor: backgroundColorList,
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            }
        }
    });
}
get_client_stats()


// session chart
async function get_session_stats() {
    const session_status_res = await fetch(session_stats_url)
    let session_status_obj = await session_status_res.json()

    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    let currentValH5 = document.querySelector("#currentNoOfSessions")
    currentValH5.textContent = Object.values(session_status_obj).slice(-1)[0]

    // let backgroundColorList =  Array.from({length:Object.values(session_status_obj).length},(v,k)=>((k+1)*15+0x000000).toString(16)).map(elem => `#55${elem}`);
    let sessionCtart = document.getElementById("sessionChart").getContext('2d');
    new Chart(sessionCtart, {
        type: 'bar',
        data: {
            labels: Object.keys(session_status_obj),
            datasets: [{
                label: '# of Sessions',
                data: Object.values(session_status_obj),
                backgroundColor: backgroundColorList,
    
            }]
        },
        options: {
            legend: {
                display: false,
                labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "black",
                        beginAtZero: true
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "black"
                    }
                }]
            }
        }
    });
}
get_session_stats()


// Sesions per Coach
async function get_sessions_per_coach_data() {

    const sessions_per_coach_res = await fetch(sessions_per_coach_url);
    let sessions_per_coach_obj = await sessions_per_coach_res.json();
    let sessionPerCoachCtart = document.getElementById("sessionPerCoachChart").getContext('2d');

    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    let currentValH5 = document.querySelector("#maxNumberOfSessionPerCoach")
    currentValH5.textContent = Object.values(sessions_per_coach_obj).slice(-1)[0]

    // let backgroundColorList =  Array.from({length:Object.values(sessions_per_coach_obj).length},(v,k)=>((k+1)*15+0x000000).toString(16)).map(elem => `#55${elem}`);
    new Chart(sessionPerCoachCtart, {
        type: 'doughnut',
        data: {
            labels: Object.keys(sessions_per_coach_obj),
            datasets: [{
                label: '# Session Per Coach',
                data: Object.values(sessions_per_coach_obj),
                backgroundColor: backgroundColorList,
    
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    fontColor: "#023047",
                    usePointStyle: true,
                },
                position: "right"
            },
    
        }
    });
}
get_sessions_per_coach_data()

// Sessions per Client
async function get_sessions_per_client_data() {

    const sessions_per_client_res = await fetch(sessions_per_client_url);
    let sessions_per_client_obj = await sessions_per_client_res.json()
    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    let currentValH5 = document.querySelector("#maxNumberOfSessionPerClient")
    currentValH5.textContent = Object.values(sessions_per_client_obj).slice(-1)[0]

    let sessionPerClientCtart = document.getElementById("sessionPerClientChart").getContext('2d');
    new Chart(sessionPerClientCtart, {
        type: 'doughnut',
        data: {
            labels: Object.keys(sessions_per_client_obj),
            datasets: [{
                label: '# Session Per Client',
                data: Object.values(sessions_per_client_obj),
                backgroundColor: backgroundColorList,
    
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    fontColor: "#023047",
                    usePointStyle: true,
                },
                position: "right"
            },
    
        }
    });
}
get_sessions_per_client_data()


// Sesions per Category
async function get_sessions_per_category_data() {

    const sessions_per_category_res = await fetch(sessions_per_category_url);
    let sessions_per_category_obj = await sessions_per_category_res.json();
    let sessionPerCategoryCtart = document.getElementById("sessionPerCategoryChart").getContext('2d');

    let backgroundColorList = ['#22A39F', '#222222', '#434242', '#F3EFE0', '#678983', '#181D31', '#88A47C']
    let currentValH5 = document.querySelector("#maxNumberOfSessionPerCategory")
    currentValH5.textContent = Object.values(sessions_per_category_obj).slice(-1)[0]

    new Chart(sessionPerCategoryCtart, {
        type: 'doughnut',
        data: {
            labels: Object.keys(sessions_per_category_obj),
            datasets: [{
                label: '# Session Per Category',
                data: Object.values(sessions_per_category_obj),
                backgroundColor: backgroundColorList,
    
            }]
        },
        options: {
            legend: {
                display: true,
                labels: {
                    fontColor: "#023047",
                    usePointStyle: true,
                },
                position: "right"
            },
    
        }
    });
}
get_sessions_per_category_data()


// customer messages
async function close_customer_message(messageId){
    let response = await fetch(
        close_customer_message_url,
        {method: 'POST',body: JSON.stringify({'message_id':messageId})}
        )
    let responseObj = await response.json()
    get_customer_messages()
}
async function get_customer_messages() {
    const customer_messages_res = await fetch(customer_messages_url);
    const customer_messages_obj = await customer_messages_res.json()
    let noOfMsgsH5 = document.querySelector('#noOfMsgs')
    let msgLstDiv = document.querySelector('#msgLst')
    msgLstDiv.textContent = ""
    noOfMsgsH5.textContent = customer_messages_obj['messages'].length

    // notifier
    if (customer_messages_obj['messages'].length == 0 ){
        document.querySelector('#notification').hidden = true;
    }


    customer_messages_obj['messages'].forEach((element, index) => {
        let listGroupItem = document.createElement('div')
        listGroupItem.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between')
        
        let listGroupItemOuterDiv = document.createElement('div')
        listGroupItemOuterDiv.classList.add('d-flex', 'flex-column', 'w-100')

        
        // upper div
        let listGroupNav = document.createElement('div')
        listGroupNav.classList.add('d-flex', 'justify-content-between')
        
        // nav left content
        let  listGroupNavLeftDiv = document.createElement('div')
        listGroupNavLeftDiv.textContent = element.full_name
        
        // nav right content
        let  listGroupNavRightDiv = document.createElement('div')

        // create display message button
        let listGroupCollapseBtn = document.createElement('button')
        listGroupCollapseBtn.classList.add('btn', 'btn-outline-warning')
        listGroupCollapseBtn.setAttribute("data-bs-toggle", "collapse")
        listGroupCollapseBtn.setAttribute("data-bs-target", `#collapse${index}`)
        let displayIcon = document.createElement('i')
        displayIcon.classList.add('fa', 'fa-eye')
        listGroupCollapseBtn.append(displayIcon)

        // create resolve button
        let listGroupResolveBtn = document.createElement('button')
        listGroupResolveBtn.classList.add('btn', 'btn-outline-success', 'me-2')
        listGroupResolveBtn.id = `resolve${element.id}`
        let resolveIcon = document.createElement('i')
        resolveIcon.classList.add('fa', 'fa-check-circle')
        listGroupResolveBtn.append(resolveIcon)
        listGroupResolveBtn.addEventListener('click', () => close_customer_message(element.id))
        
        // add buttons
        listGroupNavRightDiv.append(listGroupResolveBtn)
        listGroupNavRightDiv.append(listGroupCollapseBtn)

        // add nav content
        listGroupNav.append(listGroupNavLeftDiv)
        listGroupNav.append(listGroupNavRightDiv)

        // lower div
        let listGroupMsgDiv = document.createElement('div')
        listGroupMsgDiv.classList.add('collapse')
        listGroupMsgDiv.id = `collapse${index}`
        listGroupMsgDiv.textContent = element.message


        // add main item content
        listGroupItemOuterDiv.append(listGroupNav)
        listGroupItemOuterDiv.append(listGroupMsgDiv)
        listGroupItem.append(listGroupItemOuterDiv)

        // add item to message div
        msgLstDiv.append(listGroupItem)
        
    });

}
get_customer_messages()
setInterval(get_customer_messages, 1800000); // refresh customer messages every 30 Mins


// promo codes
async function end_promo_code(codeId){
    let response = await fetch(
        end_promo_code_url,
        {method: 'POST',body: JSON.stringify({'code_id':codeId})}
        )
    let responseObj = await response.json()
    get_promo_codes()
}

// generateNewPromoBtn
async function generateNewPromoCode(){
    let discount = document.querySelector('#discount').value
    console.log(`discount: ${discount}`)
    let response = await fetch(
        generate_new_promo_code_url,
        {method: 'POST',body: JSON.stringify({'discount':discount})}
        )
    let responseObj = await response.json()
    get_promo_codes()
}
document.querySelector('#generateNewPromoBtn').addEventListener('click', generateNewPromoCode)
async function get_promo_codes() {
    const promo_codes_res = await fetch(promo_codes_url);
    const promo_codes_obj = await promo_codes_res.json()
    console.log(promo_codes_obj)
    let noOfCodesH5 = document.querySelector('#noOfCodes')
    let promoCodeLstDiv = document.querySelector('#promoCodeList')
    promoCodeLstDiv.textContent = ""
    noOfCodesH5.textContent = promo_codes_obj['codes'].length


    // notifier
    if (promo_codes_obj['codes'].length == 0 ){
        document.querySelector('#codeNotification').hidden = true;
    }


    promo_codes_obj['codes'].forEach((element, index) => {
        let listGroupItem = document.createElement('div')
        listGroupItem.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between')
        
        let listGroupItemOuterDiv = document.createElement('div')
        listGroupItemOuterDiv.classList.add('d-flex', 'flex-column', 'w-100')

        
        // upper div
        let listGroupNav = document.createElement('div')
        listGroupNav.classList.add('d-flex', 'justify-content-between')
        
        // nav left content
        let  listGroupNavLeftDiv = document.createElement('div')
        listGroupNavLeftDiv.textContent = element.code
        

        // second div
        let listGroupSecondDiv = document.createElement('div')
        listGroupSecondDiv.textContent = `${element.value} %`

        // Third div
        let listGroupThirdDiv = document.createElement('div')
        listGroupThirdDiv.classList.add('badge', 'rounded-pill', 'bg-warning')
        listGroupThirdDiv.style.height = '50%'
        listGroupThirdDiv.textContent = `${element.used_by.length}`

        // nav right content
        let  listGroupNavRightDiv = document.createElement('div')


        // create end button
        let listGroupEndBtn = document.createElement('button')
        listGroupEndBtn.classList.add('btn', 'btn-outline-danger', 'me-2')
        listGroupEndBtn.id = `end${element.id}`
        let endIcon = document.createElement('i')
        endIcon.classList.add('fa', 'fa-trash')
        listGroupEndBtn.append(endIcon)
        listGroupEndBtn.addEventListener('click', () => end_promo_code(element.id))
        
        // add buttons
        listGroupNavRightDiv.append(listGroupEndBtn)

        // add nav content
        listGroupNav.append(listGroupNavLeftDiv)
        listGroupNav.append(listGroupSecondDiv)
        listGroupNav.append(listGroupThirdDiv)
        listGroupNav.append(listGroupNavRightDiv)


        // add main item content
        listGroupItemOuterDiv.append(listGroupNav)
        listGroupItem.append(listGroupItemOuterDiv)

        // add item to message div
        promoCodeLstDiv.append(listGroupItem)
        
    });

}
get_promo_codes()
