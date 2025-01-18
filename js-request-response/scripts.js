console.log("Testing is script file is working");

function sendRequest(prompt){
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("authorization", "Bearer sk-02e44d2ccb164c738a6c4a65dbf75e89")

    var raw = JSON.stringify({
        "question": prompt,
        "model": "aicon-v4-nano-160824",
        "randomness": 0.5,
        "stream_data": false,
        "training_data": "You are alex and you are one of the best Tour Guides. answer" +
            " everything while starting with your name and write the answer as a html code" +
            " output. no need to enclose it within backticks of codebase, just return the html" +
            " code nothing else",
        "response_type": "text"
    });

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };

    fetch("https://api.worqhat.com/api/ai/content/v4", requestOptions)
        .then(response => response.json())
        .then(result => {
            console.log(result.content);
            let outPut = (result.content);
            outPut = outPut.replace("```html", "")
            outPut = outPut.replace("```", "")
            document.getElementById("responseText").innerHTML = outPut;
        })
        .catch(error => console.log('error', error));
}

document.getElementById("sendRequest").addEventListener('click',()=>{
    const inputPrompt = document.getElementById("userInput").value;
    console.log("Input prompt is ", inputPrompt)

    sendRequest(inputPrompt)
})
