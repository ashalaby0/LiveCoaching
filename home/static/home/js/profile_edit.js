// certificates
async function remove_certificate(certId){
    console.log(certId)
    let response = await fetch(
        remove_certificate_url,
        {method: 'POST',body: JSON.stringify({'cert_id':certId})}
        )
    let responseObj = await response.json()
    getCoachCertificates()
}

// addNewCertificate
async function addNewCertificateToCoach(){
    let formdata = new FormData();  
    let certTitle = document.querySelector('#certTitle').value
    let certFile = document.querySelector('#cert').files[0]
    
    formdata.append( 'picture', certFile ); 
    formdata.append( 'name', certTitle ); 
    let response = await fetch(
        add_new_certificate_to_coach_url,
        {
            method: 'POST',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', 
              },
            body: formdata
            }
        )
    let responseObj = await response.json()
    getCoachCertificates()
}
document.querySelector('#addNewCertificate').addEventListener('click', addNewCertificateToCoach)
// TODO
// still not done yet
async function getCoachCertificates() {
    const certificates_res = await fetch(get_all_certificates_url);
    const certificates_obj = await certificates_res.json()
    console.log(certificates_obj)
    let certificateLstDiv = document.querySelector('#certificateList')
    certificateLstDiv.textContent = ""


    certificates_obj['certificates'].forEach((element, index) => {
        console.log('11111111111')
        let listGroupItem = document.createElement('div')
        listGroupItem.classList.add('list-group-item', 'list-group-item-action', 'd-flex', 'justify-content-between')
        
        let listGroupItemOuterDiv = document.createElement('div')
        listGroupItemOuterDiv.classList.add('d-flex', 'flex-column', 'w-100')

        
        // upper div
        let listGroupNav = document.createElement('div')
        listGroupNav.classList.add('d-flex', 'justify-content-between')
        
        // nav left content
        let  listGroupNavLeftDiv = document.createElement('div')
        listGroupNavLeftDiv.textContent = element.name
        

        // second div
        let listGroupSecondDiv = document.createElement('div')
        let secondDivImg = document.createElement('img')
        secondDivImg.src = element.picture
        secondDivImg.alt = "Cert Image"
        secondDivImg.height = "25"
        secondDivImg.width = "30"
        secondDivImg.style.borderRadius = "50%"

        listGroupSecondDiv.append(secondDivImg)


        // nav right content
        let  listGroupNavRightDiv = document.createElement('div')


        // create remove button
        let listGroupEndBtn = document.createElement('button')
        listGroupEndBtn.classList.add('btn', 'btn-outline-danger', 'me-2')
        listGroupEndBtn.setAttribute('type', 'button')
        listGroupEndBtn.id = `end${element.id}`
        let removeIcon = document.createElement('i')
        removeIcon.classList.add('fa', 'fa-trash')
        listGroupEndBtn.append(removeIcon)
        listGroupEndBtn.addEventListener('click', () => remove_certificate(element.id))
        
        // add buttons
        listGroupNavRightDiv.append(listGroupEndBtn)

        // add nav content
        listGroupNav.append(listGroupNavLeftDiv)
        listGroupNav.append(listGroupSecondDiv)
        listGroupNav.append(listGroupNavRightDiv)


        // add main item content
        listGroupItemOuterDiv.append(listGroupNav)
        listGroupItem.append(listGroupItemOuterDiv)

        // add item to message div
        certificateLstDiv.append(listGroupItem)
        
    });

}
getCoachCertificates()
