let _joinUrl = document.querySelector('#meeting_number').attributes['data-url'].value;
console.log(_joinUrl)

window.addEventListener('DOMContentLoaded', function(event) {
  console.log('DOM fully loaded and parsed');
  websdkready();
});

function websdkready() {
  var testTool = window.testTool;
  if (testTool.isMobileDevice()) {
    vConsole = new VConsole();
  }
  console.log("checkSystemRequirements");
  console.log(JSON.stringify(ZoomMtg.checkSystemRequirements()));

  ZoomMtg.preLoadWasm(); // pre download wasm file to save time.
 
  // some help code, remember mn, pwd, lang to cookie, and autofill.
  document.getElementById("display_name").value =
    "CDN" +
    ZoomMtg.getJSSDKVersion()[0] +
    testTool.detectOS() +
    "#" +
    testTool.getBrowserInfo();
  document.getElementById("meeting_number").value = testTool.getCookie(
    "meeting_number"
  );
  document.getElementById("meeting_pwd").value = testTool.getCookie(
    "meeting_pwd"
  );
  if (testTool.getCookie("meeting_lang"))
    document.getElementById("meeting_lang").value = testTool.getCookie(
      "meeting_lang"
    );

  // get sdk creds
  let getSdk = async function(){
    const response = await fetch(document.querySelector('#navbar').attributes['data-url'].value, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    const data = await response.json();
    return data;
  };
  
  // click join meeting button
  document
    .getElementById("join_meeting")
    .addEventListener("click", async function (e) {
      e.preventDefault();
      var meetingConfig = testTool.getMeetingConfig();

      meetingConfig.mn = document.querySelector('#meeting_number').value
      meetingConfig.pwd = document.querySelector('#meeting_pwd').value
      meetingConfig.role = '0'

      // get creds
      let rslt = await getSdk()
      console.log(rslt)
      testTool.setCookie("meeting_number", meetingConfig.mn);
      testTool.setCookie("meeting_pwd", meetingConfig.pwd);

      console.log(rslt.key)
      console.log(rslt.pass)
    var signature = ZoomMtg.generateSDKSignature({
        meetingNumber: meetingConfig.mn, // meeting number 
        sdkKey: rslt.key, // key
        sdkSecret: rslt.pass, // secret
        role: meetingConfig.role, // rol ( Attendee, Host)
        success: function (res) {
          console.log(res.result);
          meetingConfig.signature = res.result;
          meetingConfig.sdkKey = rslt.key;   // key
          var joinUrl = `${_joinUrl}?${testTool.serialize(meetingConfig)}`;
          console.log(joinUrl);
          window.open(joinUrl, "_blank");
        },
      });
    });

  function copyToClipboard(elementId) {
    var aux = document.createElement("input");
    aux.setAttribute("value", document.getElementById(elementId).getAttribute('link'));
    document.body.appendChild(aux);  
    aux.select();
    document.execCommand("copy");
    document.body.removeChild(aux);
  }
    
}
