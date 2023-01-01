let _joinUrl = document.querySelector('.join_meeting').attributes['data-url-jn'].value;

window.addEventListener('DOMContentLoaded', function (event) {
  console.log('DOM fully loaded and parsed');
  websdkready();

});

async function  websdkready() {
  var testTool = window.testTool;
  if (testTool.isMobileDevice()) {
    vConsole = new VConsole();
  }
  console.log("checkSystemRequirements");
  console.log(JSON.stringify(ZoomMtg.checkSystemRequirements()));

  ZoomMtg.preLoadWasm(); // pre download wasm file to save time.

  // get sdk creds
  let getSdk = async function () {
    const response = await fetch(document.querySelector('.join_meeting').attributes['data-url-embd'].value, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });
    const data = await response.json();
    return data;
  };

  let redirectToMeeting = async function () {
    console.log('getting meeting data')
    let meetingConfig = await testTool.getMeetingConfig();
    console.log('got meeting data')
    console.log(`Data mn: ${meetingConfig.mn}`)
    console.log(`Data pwd: ${meetingConfig.pwd}`)
    console.log(`Data role: ${meetingConfig.role}`)
    console.log(`serialized meetingConfig: ${testTool.serialize(meetingConfig)}`)

    // get creds
    let rslt = await getSdk()
    console.log(`result: ${rslt}`)
    testTool.setCookie("meeting_number", meetingConfig.mn);
    testTool.setCookie("meeting_pwd", meetingConfig.pwd);

    console.log(`key: ${rslt.key}`)
    console.log(`pass: ${rslt.pass}`)
    let signature = ZoomMtg.generateSDKSignature({
      meetingNumber: meetingConfig.mn, // meeting number 
      sdkKey: rslt.key, // key
      sdkSecret: rslt.pass, // secret
      role: meetingConfig.role, // rol ( Attendee 0, Host 1)
      success: function (res) {
        console.log(res.result);
        meetingConfig.signature = res.result;
        meetingConfig.sdkKey = rslt.key;   // key
        var joinUrl = `${_joinUrl}?${testTool.serialize(meetingConfig)}`;
        window.open(joinUrl, "_self");
      },
    });
  };
  await redirectToMeeting()
}
