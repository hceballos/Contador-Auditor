<?php

$field_name = $_POST['cf_name'];

$field_email = $_POST['cf_email'];

$field_message = $_POST['cf_message'];



$mail_to = 'ceballosaviles@gmail.com';

$subject = 'Mensaje de un visitante del sitio promotoras '.$field_name;



$body_message = 'From: '.$field_name."\n";

$body_message .= 'E-mail: '.$field_email."\n";

$body_message .= 'Message: '.$field_message;



$headers = 'From: '.$field_email."\r\n";

$headers .= 'Reply-To: '.$field_email."\r\n";



$mail_status = mail($mail_to, $subject, $body_message, $headers);



if ($mail_status) { ?>

	<script language="javascript" type="text/javascript">

		alert('Gracias por el mensaje. Me pondré en contacto con usted en breve.');

		window.location = 'index.html';

	</script>

<?php

}

else { ?>

	<script language="javascript" type="text/javascript">

		alert('Mensaje falló. Por favor , envíe un correo electrónico a ceballosaviles@gmail');

		window.location = 'index.html';

	</script>

<?php

}

?>