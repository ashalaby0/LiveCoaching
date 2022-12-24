/* coach sorting
---------------------------------------- */
let loadSortedCoaches = async function(item) {
    let  coach_name_q = document.querySelector('#nameInput').value
    if (coach_name_q == '') {
        coach_name_q = 'Empty'
    }
    let  coach_speciality_q = document.querySelector('#specialityInput').value
    if (coach_speciality_q == '') {
        coach_speciality_q = 'Empty'
    }
    let  min_price_q = document.querySelector('#minPriceInput').value
    let  max_price_q = document.querySelector('#maxPriceInput').value
    let  coach_list_div = document.querySelector('#coach-list')
    let  url = item.attributes['value'].value.replace('coach_name_q', coach_name_q).replace('coach_speciality_q', coach_speciality_q).replace('min_price_q', min_price_q).replace('max_price_q', max_price_q)

    const response = await fetch(url, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      const data = await response.json();
      console.log(data)
      parsed_json = data['sorted_coaches']
    //   parsed_json = JSON.parse(data['sorted_coaches'])
      console.log(parsed_json)
      

    coach_list_div.textContent = ''

    parsed_json.forEach(
        (item) => {
            // here we recreate the coaches page
            // outer div
            let new_coach_div = document.createElement('div')
            // first inner div
            let new_coach_div1 = document.createElement('div')
            new_coach_div1.classList.add('card', 'custom-text-primary', 'mb-3')
            new_coach_div.append(new_coach_div1)

            // second inner div
            let new_coach_div2 = document.createElement('div')
            new_coach_div2.classList.add('card-body', 'd-flex', 'justify-content-between')
            new_coach_div1.append(new_coach_div2)

            // third inner div
            let new_coach_div3 = document.createElement('div')
            new_coach_div3.classList.add('d-flex', 'justify-content-between')
            new_coach_div2.append(new_coach_div3)

            // tooltip div
            let tooltip_div = document.createElement('div')
            tooltip_div.setAttribute('data-bs-toggle', 'tooltip')
            tooltip_div.setAttribute('title', 'Coach Profile')
            let tootltip_anchor = document.createElement('a')
            let tooltip_href = coach_details_url.replace('1111', item.id)
            tootltip_anchor.setAttribute('href', tooltip_href)
            let anchor_img = document.createElement('img')
            console.log(item.photo)
            anchor_img.setAttribute('src', item.photo)
            anchor_img.classList.add('coach-img', 'img-fluid')
            anchor_img.setAttribute('alt', 'coach-img')
            tootltip_anchor.append(anchor_img)
            tooltip_div.append(tootltip_anchor)
            new_coach_div3.append(tooltip_div)
            
            // main info div
            let main_info_div = document.createElement('div')
            let coach_name_h4 = document.createElement('h4')
            coach_name_h4.textContent = item.user
            main_info_div.append(coach_name_h4)
            let coach_speciality = document.createElement('p')
            coach_speciality.textContent = item.speciality
            main_info_div.append(coach_speciality)

            let rating_div = document.createElement('div')
            Array(item.rating).fill(1).forEach(
                () => {
                    let starI = document.createElement('i')
                    starI.classList.add('fa-solid', 'fa-star')
                    starI.style.color = 'gold'
                    rating_div.append(starI)
                }
            )
            main_info_div.append(rating_div)

            // location icon
            let locationDiv = document.createElement('div')
            let localtionIcon = document.createElement('i')
            localtionIcon.classList.add('bi', 'bi-geo-alt-fill')
            locationDiv.append(localtionIcon)
            let locationSpan = document.createElement('span')
            locationSpan.textContent = item.location 
            locationDiv.append(locationSpan)
            
            new_coach_div3.append(main_info_div)

            // middle info div
            let middleInfoDiv =  document.createElement('div')
            let avilDiv =  document.createElement('div')
            avilDiv.classList.add('m-2')
            let avilIcon =  document.createElement('i')
            avilIcon.classList.add('bi', 'bi-universal-access')
            avilDiv.append(avilIcon)
            let avilSpan = document.createElement('span')

            if (item.available_for_kids == 'False') {
                avilSpan.textContent = 'Not Available For Kids'
            }
            else{
                avilSpan.textContent = 'Available For Kids'
            }
            avilDiv.append(avilSpan)
            middleInfoDiv.append(avilDiv)

            // price per hour
            let pricePerHourDiv = document.createElement('div')
            pricePerHourDiv.classList.add('m-2')
            let pricePerHourIcon = document.createElement('i')
            pricePerHourIcon.classList.add('bi', 'bi-cash')
            pricePerHourDiv.append(pricePerHourIcon)
            let pricePerHourSpan = document.createElement('span')
            pricePerHourSpan.textContent = `${item.price_per_hour} per hour.`
            pricePerHourDiv.append(pricePerHourSpan)
            middleInfoDiv.append(pricePerHourDiv)
            
            
            // price per 30 mins
            let pricePer30MinsDiv = document.createElement('div')
            pricePer30MinsDiv.classList.add('m-2')
            let pricePer30MinsIcon = document.createElement('i')
            pricePer30MinsIcon.classList.add('bi', 'bi-cash')
            pricePer30MinsDiv.append(pricePer30MinsIcon)
            let pricePer30MinsSpan = document.createElement('span')
            pricePer30MinsSpan.textContent = `${item.price_per_30_mins} per 30 min.`
            pricePer30MinsDiv.append(pricePer30MinsSpan)
            middleInfoDiv.append(pricePer30MinsDiv)

            new_coach_div2.append(middleInfoDiv)

            // rightInfoDiv

            let rightInfoDiv = document.createElement('div')
            let coachProfileDiv = document.createElement('div')
            coachProfileDiv.classList.add('d-flex', 'flex-column', 'gap-2')

            // view profile
            let viewProfileDiv = document.createElement('div')
            viewProfileDiv.classList.add('w-100')
            let viewProfileAnchor = document.createElement('a')
            viewProfileAnchor.classList.add('btn', 'custom-btn-outline-primary')
            let viewProfile_href = coach_details_url.replace('1111', item.id)
            viewProfileAnchor.setAttribute('href', viewProfile_href)
            viewProfileDiv.append(viewProfileAnchor)
            let viewProfileSpan = document.createElement('span')
            viewProfileSpan.textContent = 'VIEW COACH PROFILE'
            viewProfileAnchor.append(viewProfileSpan)
            coachProfileDiv.append(viewProfileDiv)

            // book appointment
            let bookAppointmentDiv = document.createElement('div')
            bookAppointmentDiv.classList.add('w-100')
            let bookAppointmentAnchor = document.createElement('a')
            bookAppointmentAnchor.classList.add('btn', 'custom-btn-primary', 'w-100')
            let bookAppointment_href = booking_url.replace('1111', item.id)
            bookAppointmentAnchor.setAttribute('href', bookAppointment_href)
            bookAppointmentDiv.append(bookAppointmentAnchor)
            let bookAppointmentSpan = document.createElement('span')
            bookAppointmentSpan.textContent = 'BOOK APPOINTMENT'
            bookAppointmentAnchor.append(bookAppointmentSpan)
            coachProfileDiv.append(bookAppointmentDiv)

            rightInfoDiv.append(coachProfileDiv)

            new_coach_div2.append(rightInfoDiv)


            // continue adding rest of coach card content here
            
            coach_list_div.append(new_coach_div)
            console.log('new h1 added')
        }
      )
      return data;
}


let sortingOptions = document.querySelectorAll('.coach-sorting-option')
sortingOptions.forEach(
    (item) => {
        item.addEventListener('click', () => loadSortedCoaches(item))
    }
)