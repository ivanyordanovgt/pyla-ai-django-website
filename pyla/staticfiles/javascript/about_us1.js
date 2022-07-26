const whatIsPyla = document.getElementById('whatIsPyla')
const whatIsPylaDesc = document.getElementById('desc')
const [desc, escanorImage, vidLabel, youtubeVid] = whatIsPylaDesc.children;
const descText = desc.textContent;
const pylaBoxDiv = document.getElementsByClassName('about-pyla-box')[0]

// whatIsPyla.addEventListener('mouseover', () => {
//
//     whatIsPyla.style.fontFamily = 'Monaco, "Courier New", Courier, monospace'
    //     whatIsPyla.textContent = 'Click me'
    // })
    //
    // whatIsPyla.addEventListener('mouseout', () => {
    //
    //     whatIsPyla.style.fontFamily = ''
    //     whatIsPyla.textContent = 'What is    PyLa?'
// })




whatIsPylaDesc.style.display = '';
desc.textContent = '';
whatIsPyla.style.display = 'none';
escanorImage.style.display = 'none';
vidLabel.style.display = 'none';
let timeOut = 370;
let textAnimationFinishTimeOut = timeOut+(50*(descText.length));

setTimeout(() => {
    // escanorImage.style.display = '';
    vidLabel.style.display = '';
    escanorImage.style.opacity = 0.0;
    let timeOutCurrent = 100;

    for (let i = 1; i < 50; i++) {
        setTimeout(() => {
            escanorImage.style.opacity = i/100;
        }, timeOutCurrent)

        timeOutCurrent += 40;

    }

}, textAnimationFinishTimeOut)

for (let index = 0; index < descText.length; index++) {

    setTimeout(() => {
        desc.textContent += descText[index]
    }, timeOut);
    timeOut += 100;

}


vidLabel.addEventListener('mouseover', gameplayAnimation)

function gameplayAnimation() {
    youtubeVid.style.display = '';
    desc.style.display = 'none';
    escanorImage.style.display = 'none';
    vidLabel.style.marginTop = '4vw'
    vidLabel.style.color = 'peachpuff'
    let timeOut = 2000;
    const messages = ['PyLa is entirely written in Python', 'She uses an object detection alg coded by me', 'That works with OpenCV', 'Keep in mind that!', 'PyLa is in her very early stages.', 'A lot of improvement is to come', 'Thanks for the early support', '<3']
    pylaBoxDiv.style.marginTop = '10vw'

    for (let message of messages) {
        setTimeout(() => {
            vidLabel.textContent = message;

        }, timeOut)
        timeOut += 2000;
    }

    vidLabel.removeEventListener('mouseover', gameplayAnimation)

    infoApp.createInfoPanel()
}
