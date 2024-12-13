var socket;
    $(document).ready(function(){
        
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
            socket.emit('joined', {});
        });
        
        socket.on('status', function(data) {     
            let tag  = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);

        });      
        socket.on('message', function(data) {
            let tag = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat");
            tag.appendChild(text);
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });
    
        // Handle sending a message
        $('#send-button').click(function() {
            let messageInput = $('#message-input');
            let message = messageInput.val().trim();
            if (message) {
                socket.emit('message', { msg: message });
                messageInput.val(''); // Clear the input field after sending
            }
        });
    
        // Handle leaving the chat room
        $('#leave-button').click(function() {
            socket.emit('left', {});
            window.location.href = '/home';
        });
      
    });