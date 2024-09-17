function display_message(title, message, type = 'success', duration = 5000) {
    const messageArea = document.getElementById('system-message-area');
    const messageBox = document.createElement('div');
    messageBox.className = 'system-message-box pointer-events-auto w-full overflow-hidden bg-gray-900 rounded-lg shadow-lg ring-1 ring-white ring-opacity-20 transform translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2';
    
    const icons = {
        success: `<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
        </svg>`,
        info: `<svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd" />
        </svg>`,
        warning: `<svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
        </svg>`,
        error: `<svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
        </svg>`
    };

    const icon = icons[type] || icons.success;
    
    messageBox.innerHTML = `
        <div class="p-4">
            <div class="flex items-start">
                <div class="flex-shrink-0">
                    ${icon}
                </div>
                <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="text-sm font-medium text-white">${title}</p>
                    <p class="mt-1 text-sm text-gray-500">${message}</p>
                </div>
                <div class="ml-4 flex flex-shrink-0">
                    <button type="button"
                        class="system-message-box-close-button inline-flex rounded-md text-gray-500 hover:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                        <span class="sr-only">Close</span>
                        <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path
                                d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="progress-bar-container w-full h-0.5 bg-gray-700">
            <div class="progress-bar h-full bg-green-500 transition-all duration-100 ease-linear" style="width: 100%;"></div>
        </div>
    `;

    messageArea.appendChild(messageBox);

    // Trigger entering animation
    setTimeout(() => {
        messageBox.classList.add('transition', 'transform', 'ease-out', 'duration-300');
        messageBox.classList.remove('translate-y-2', 'opacity-0', 'sm:translate-y-0', 'sm:translate-x-2');
        messageBox.classList.add('translate-y-0', 'opacity-100', 'sm:translate-x-0');
    }, 10);

    const progressBar = messageBox.querySelector('.progress-bar');
    let timeLeft = duration;
    const intervalTime = 100; // Update every 100ms for smoother animation

    const updateProgressBar = () => {
        timeLeft -= intervalTime;
        const width = (timeLeft / duration) * 100;
        progressBar.style.width = `${width}%`;

        if (timeLeft <= 0) {
            clearInterval(progressInterval);
            closeMessageBox();
        }
    };

    const progressInterval = setInterval(updateProgressBar, intervalTime);

    // Function to handle closing the message box
    const closeMessageBox = () => {
        clearInterval(progressInterval);
        // Trigger leaving animation
        messageBox.classList.remove('transition', 'transform', 'ease-out', 'duration-300');
        messageBox.classList.add('transition', 'ease-in', 'duration-100');
        messageBox.classList.remove('translate-y-0', 'opacity-100', 'sm:translate-x-0');
        messageBox.classList.add('translate-y-2', 'opacity-0', 'sm:translate-y-0', 'sm:translate-x-2');

        // Remove the message box after animation
        setTimeout(() => {
            if (messageArea.contains(messageBox)) {
                messageArea.removeChild(messageBox);
            }
        }, 100);
    };

    // Add event listener for close button
    const closeButton = messageBox.querySelector('.system-message-box-close-button');
    closeButton.addEventListener('click', closeMessageBox);

    // Automatically remove the message after the specified duration
    setTimeout(closeMessageBox, duration);
}

// Message Queue
const eventSource = new EventSource("/stream");

// Event handler mapping
const eventHandlers = {
    "queue_status_update": handleQueueStatus,
    "display_message": handleDisplayMessage
};

eventSource.addEventListener('broadcast', function(event) {
    const data = JSON.parse(JSON.parse(event.data));

    if (data.event && eventHandlers[data.event]) {
        eventHandlers[data.event](data);
    } else {
        display_message("Error parsing backend event", "No handler configured for event type: " + data.event, "error", 10000)
    }
});

eventSource.onerror = function(error) {
    console.error("EventSource failed:", error);
    eventSource.close();
};


// Queue status handling

const STATUS_CONFIG = {
    Invalid: {
        text: "Idle",
        bgClass: "bg-gray-900",
        textClass: "text-gray-300"
    },
    Searching: {
        text: "In Queue",
        bgClass: "bg-blue-600",
        textClass: "text-white"
    },
    Found: {
        text: "Match Found",
        bgClass: "bg-yellow-600",
        textClass: "text-white"
    },
    // Add more status configurations here
    default: {
        bgClass: "bg-gray-900",
        textClass: "text-gray-300"
    }
};

// Helper function to update classes
function updateClasses(element, newClass, prefix) {
    // Remove all classes that start with the prefix
    element.classList.forEach(cls => {
        if (cls.startsWith(prefix)) {
            element.classList.remove(cls);
        }
    });
    // Add the new class
    element.classList.add(newClass);
}

function handleQueueStatus(event) {
    const queueStatusText = document.getElementById('queue-status-text');
    const queueStatusBackground = document.getElementById('queue-status-background');
    
    const status = event.data.status;
    const config = STATUS_CONFIG[status] || STATUS_CONFIG.default;

    queueStatusText.innerText = config.text || status;
    
    // Update background class
    updateClasses(queueStatusBackground, config.bgClass, 'bg-');
    
    // Update text class
    updateClasses(queueStatusText, config.textClass, 'text-');
}

function handleDisplayMessage(event) {
    if (!event.data.hasOwnProperty("duration")) {
        event.data.duration = 5000;
    }
    display_message(event.data.title, event.data.message, event.data.type, event.data.duration);
}