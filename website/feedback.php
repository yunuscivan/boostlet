<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = htmlspecialchars($_POST["name"]);
    $email = htmlspecialchars($_POST["email"]);
    $message = htmlspecialchars($_POST["message"]);

    $to = "yunuscivan06@gmail.com";
    $subject = "New Feedback from Boostlet Website";
    $body = "Name: $name\nEmail: $email\n\nMessage:\n$message";
    $headers = "From: $email";

    if (mail($to, $subject, $body, $headers)) {
        echo "<script>
                alert('Thank you for your feedback!');
                window.location.href = 'feedback.html';
              </script>";
    } else {
        echo "<script>
                alert('Sorry, something went wrong.');
                window.location.href = 'feedback.html';
              </script>";
    }
}
?>