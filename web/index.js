addEventListener('load', () => {

    fillAgentList();

    initiateSkewScroll();

    // EEL EXPOSING
    eel.expose( alertUser );
    eel.expose( askUserToChooseAgent );
    eel.expose( changeStatus );
    eel.expose( hideStopButton )

    console.log("010101110110100001100101011011100010000001101100011010010110011001100101001000000110011101101001011101100110010101110011001000000111100101101111011101010010000001101100011001010110110101101111011011100111001100101100001000000110110101100001011010110110010100100000011011000110010101101101011011110110111001100001011001000110010100101110") // 010101110110100001100101011011100010000001101100011010010110011001100101001000000110011101101001011101100110010101110011001000000111100101101111011101010010000001101100011001010110110101101111011011100111001100101100001000000110110101100001011010110110010100100000011011000110010101101101011011110110111001100001011001000110010100101110
})

function fillAgentList() {

    fetch("./json/agents.json")
    .then((response) => response.json())
    .then((agentJSON) => {
        
        let agents = Object.keys( agentJSON );

        for (const agent of agents) {

            let agent_div = document.createElement("div");
            agent_div.className = "agent";
            agent_div.id = agent;

            agent_div.setAttribute('onclick', `pickAgent('${agent}')`);
    
            let agent_div_thumbnail = document.createElement("img");
            agent_div_thumbnail.className = "agent-thumb";
            agent_div_thumbnail.src = `./assets/images/agent-banners/${ agent.toLowerCase() }.png`;
    
            let agent_div_name = document.createElement("p");
            agent_div_name.innerText = agent;

            agent_div.appendChild( agent_div_thumbnail );
            agent_div.appendChild( agent_div_name );

            document.getElementById("agents").appendChild(agent_div);

        }

    })

}

function alertUser(statusText = '', chosenAgentText = '') {

    let status = document.getElementById('status');
    let chosenAgent = document.getElementById('chosen-agent');
    let agent_preview = document.getElementById('agent-preview');

    agent_preview.src ='./assets/images/slurp.gif'; // schlurp
    status.innerText = statusText;
    chosenAgent.innerText = chosenAgentText;
    
}

function askUserToChooseAgent() {

    let status = document.getElementById('status');
    let chosenAgent = document.getElementById('chosen-agent');
    let agent_preview = document.getElementById('agent-preview');
 
    agent_preview.src ='./assets/images/slurp.gif'; // schlurp
    status.innerText = "CHOOSE AN AGENT";
    chosenAgent.innerText = "..."

}

function changeStatus(status) {

    document.getElementById('status').innerText = status;

}

function initiateSkewScroll() {

    const section = document.querySelector('#agents');

    let currentPos = section.scrollTop;

    const update = () => {
        const newPos = section.scrollTop;
        const diff = newPos - currentPos;
        const speed = diff * 0.3;
        
        section.style.transform = `skewY(${ speed }deg)`;
        
        currentPos = newPos;
        requestAnimationFrame(update);
    }

    update();

}

function pickAgent( agent ) {

    document.getElementById('status').innerText = "WAITING FOR PRE-GAME"
    document.getElementById('chosen-agent').innerText = agent.toUpperCase();
    document.getElementById('agent-preview').src = `./assets/images/agent-previews/${ agent.toLowerCase()}-preview.gif`;
    showStopButton();
    eel.try_lock(agent);

}

function showStopButton() {

    const button = bootstrap.Collapse.getOrCreateInstance( document.getElementById("stop-button-flex-row") );
    button.show();

}

function hideStopButton() {

    const button = bootstrap.Collapse.getOrCreateInstance( document.getElementById("stop-button-flex-row") );
    button.hide();

}

function stopLocking() {

    eel.stop_lock();
    askUserToChooseAgent();

}