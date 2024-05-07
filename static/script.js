$(document).ready(function () {
    let $form = $('#guess-form');
    let $input = $('input[name="guess"]');
    let $submitButton = $('button');
    let remainingTime = 60; // Initial time limit in seconds
    let submittedWords = new Set();

    // Function to update the timer display
    function updateTimer() {
        $('#timer').text(remainingTime);
    }

    // Function to disable the form and input field when time limit is reached
    function disableForm() {
        $submitButton.attr('disabled', true);
        $input.attr('disabled', true);
    }

    // Start the timer countdown
    let countdown = setInterval(function () {
        remainingTime--;
        updateTimer();

        if (remainingTime <= 0) {
            clearInterval(countdown); // Stop the countdown timer
            disableForm(); // Disable the form submission

            $('#message').text('Time is up! Refresh the page to play again!');
            updateAndRetrieveHighScore(); // Update the high score display
        }
    }, 1000); // Update the timer every second (1000 milliseconds)


    // Function to update and retrieve the high score
    async function updateAndRetrieveHighScore() {
        try {
            // Make an AJAX request to update the high score
            const currentScore = parseInt($('#score').text());
            const responseUpdate = await axios.post('/high-score', { score: currentScore });
            console.log(currentScore);

            // If the high score was updated successfully, retrieve it
            if (responseUpdate.data.isHighScore) {
                // Make an AJAX request to get the updated high score
                const responseGet = await axios.get('/high-score');
                console.log('High score retrieved:', responseGet.data);

                // Retrieve the high score from the response
                const highScore = responseGet.data.high_score;

                // Update the high score display on the page
                $('#high-score').text(highScore);
            }
        } catch (error) {
            console.error('Error updating and retrieving high score:', error);
        }
    }


    $form.submit(async function (e) {
        e.preventDefault(); // Prevent the default form submission behavior

        if (remainingTime > 0) { // Check if time limit is not yet reached
            let guess = $input.val().toUpperCase(); // Get the value of the guess input field

            // Check if the guess is already submitted
            if (submittedWords.has(guess)) {
                console.log('Word already submitted:', guess);
                return; // Exit the function
            }

            console.log('Guess:', guess);

            try {
                // Make an AJAX request using axios and await its response
                const response = await axios.post('/guess', { guess: guess });

                // Handle the response from the server
                console.log('Response from server:', response.data);

                // Update the message on the page with the response from the server
                $('#message').text(`${guess} is ${response.data.result}`);

                if (response.data.result === 'ok') {
                    let currentScore = parseInt($('#score').text()); // Get the current score and convert it to a number
                    let newScore = currentScore + guess.length; // Calculate the new score

                    $('#score').text(newScore); // Update the text content of #score with the new score
                    console.log('Score:', newScore); // Log the new score to the console
                }

                // Add the guess to the set of submitted words
                submittedWords.add(guess);

                // Clear the input field after successful submission
                $input.val('');
            } catch (error) {
                // Handle errors if the AJAX request fails
                console.error('Error:', error);
            }
        }
        updateAndRetrieveHighScore(); // Update the high score display
    });
});



