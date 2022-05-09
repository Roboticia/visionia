var pc = null;

function negotiate() {
    pc.addTransceiver('video', {direction: 'recvonly'});
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
                mode: 'usual',
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert(e);
    });
}

function start() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    if (document.getElementById('use-stun').checked) {
        config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
    }
    pc = new RTCPeerConnection(config);

    // connect audio / video
    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video') {
            document.getElementById('video').srcObject = evt.streams[0];
        }
    });
    negotiate();

    document.getElementById('stun').style.display = 'none';
    document.getElementById('start').style.display = 'none';

    //document.getElementById('stop').style.display = 'inline-block';

    document.getElementById('Texp').style.display = 'inline-block';
    document.getElementById('exp').style.display = 'inline-block';
    document.getElementById('changedata').style.display = 'inline-block';
    //document.getElementById('lapply').style.display = 'inline-block';
    document.getElementById('Tlum').style.display = 'inline-block';
    document.getElementById('lum').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';

    // close peer connection
    setTimeout(function() {
        pc.close();
    }, 500);
}


function changeExpo() {

    var input = document.getElementById("expo").value;
    console.log(input);

}

$(document).on('click', '.number-spinner button', function () {
	var btn = $(this),
		oldValue = btn.closest('.number-spinner').find('input').val().trim(),
		newVal = 0;

	if (btn.attr('data-dir') == 'up') {
		newVal = parseInt(oldValue) + 1;
	} else {
		if (oldValue > 1) {
			newVal = parseInt(oldValue) - 1;
		} else {
			newVal = 1;
		}
	}
	btn.closest('.number-spinner').find('input').val(newVal);
});
var $changedInput = $("#changedInput")

$changedInput.on("change", function (event) {
    $valueOnChange.html($(event.target).val())
})
