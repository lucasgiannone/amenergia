<?php
// header('Content-Type: text/html; charset=UTF-8');
//FIM XLS
require './SYSTOOLS/phpmailer/autoload.php';
use PHPMailer\PHPMailer\PHPMailer;
use PhpOffice\PhpSpreadsheet\Writer\Xlsx;

date_default_timezone_set('America/Sao_Paulo');
$datetime = date('Y-m-d H.i');
$date = date('Y-m-d');
$path = LOCAL;
$path = utf8_decode($path);
$folder = str_replace("/", "", $folder);
if (!file_exists($path . '/' . $date)) {
    mkdir($path . '/' . $date, 0777, true);
}

$contxls++;
$contxls++;

$arrayrplc = array(
    '/',
    '\\',
    ':',
    '*',
    '"',
    '<',
    '>',
    '|',
);

if (isset($CONCESS)) {
    $sheet->setCellValue('A' . ($contxls + 1), "Concessionaria: " . $CONCESS);
    $CONCESS = str_replace($arrayrplc, ' ', $CONCESS);
} else {
    $CONCESS = $folder;
}
$contxls++;
$sheet->setCellValue('A' . ($contxls + 1), "Data de Implantação: " . $date);
$contxls++;
$sheet->setCellValue('A' . ($contxls + 1), "Responsável: " . COD);
$contxls++;
if (isset($maior_dif)) {
    $Maior_Dif = $maior_dif;
}
if (isset($maiorDiferenca)) {
    $Maior_Dif = $maiorDiferenca;
}
if ($Maior_Dif > 0) {
    $contxls++;
    $sheet->setCellValue('A' . ($contxls + 1), "Maior Diferença Achada " . number_format($Maior_Dif, 2, ",", "."));
    $sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');
}
$contxls++;
if (isset($menor_dif)) {
    $Menor_Dif = $menor_dif;
}
if (isset($menorDiferenca)) {
    $Menor_Dif = $maiorDiferenca;
}
if ($Menor_Dif < 0) {
    $sheet->setCellValue('A' . ($contxls + 1), "Menor Diferença Achada " . number_format($Menor_Dif, 2, ",", "."));
    $sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');
}
$contxls++;
$sheet->setCellValue('A' . ($contxls + 1), "Qtde CNPJ diferente " . $cnpj_diferente);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');

$contxls++;
//erro
if (isset($class_errada)) {
    $sheet->setCellValue('A' . ($contxls + 1), "Classificação não comercial " . $class_errada);
    $sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');
}

$contxls++;
$sheet->setCellValue('A' . ($contxls + 1), "Empresa Diferente " . $empresa_diferente);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');

$contxls++;
//erro
if (isset($com_dt_emissao)) {
    $sheet->setCellValue('A' . ($contxls + 1), "Com data de emissão " . $com_dt_emissao);
    $sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');
}

$contxls++;
//erro
if (isset($sem_dt_emissao)) {
    $sheet->setCellValue('A' . ($contxls + 1), "Sem data de emissão " . $sem_dt_emissao);
    $sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');
}

$contxls++;
if (isset($tot_dif_achado)) {
    $Tot_Dif_Achado = $tot_dif_achado;
}
if (isset($menorDiferenca)) {
    $Tot_Dif_Achado = $totalComDiferenca;
}
$sheet->setCellValue('A' . ($contxls + 1), "Total de faturas com diferença " . $Tot_Dif_Achado);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');

$contxls++;
if (isset($fatsInseridas)) {
    $fat_exist_geral = $fatsInseridas;
}
$sheet->setCellValue('A' . ($contxls + 1), "Faturas existentes " . $fat_exist_geral);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');

$contxls++;
if (isset($unidadeNaoExiste)) {
    $total_nao_existe = $unidadeNaoExiste;
}
$sheet->setCellValue('A' . ($contxls + 1), "Unidades não existentes " . $total_nao_existe);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');

$contxls++;
if (isset($totalNaoInseridas)) {
    $total_nao_inserida = $totalNaoInseridas;
}
$sheet->setCellValue('A' . ($contxls + 1), "Faturas não inseridas " . $total_nao_inserida);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');

$contxls++;
if (isset($fatsInseridas)) {
    $fat_novas_geral = $fatsInseridas;
}
$sheet->setCellValue('A' . ($contxls + 1), "Faturas inseridas " . $fat_novas_geral);
$sheet->getStyle('A' . ($contxls + 1))->getFont()->getColor()->setRGB('0000FF');

if (isset($tot_dif_achado)) {
    $totalDiferencas = $tot_dif_achado;
} else {
    $totalDiferencas = $Tot_Dif_Achado;
}

//<head><meta charset="UTF-8"></head>
$html = MAILTEXT;
$html .= file_get_contents(ASSINATURA);

for ($i = 'A'; $i !== 'AB'; $i++) {
    $sheet->getColumnDimension($i)->setAutoSize(true);
}
if (!isset($printxls)) {
    $printxls = false;
}
/*$printxls = true;
$sendmail = true;*/

if ((isset($_POST["insere"]) && $_POST["insere"] != "") || ($printxls == true)) {

    $sep = utf8_decode(' ' . $separacao . 'ª Separação');
    $dt = date_parse($mes_ref);
    $y = substr($dt["year"], 2, 2);
    if (strlen($dt["month"]) < 2) {
        $m = '0' . $dt["month"];
    } else {
        $m = $dt["month"];
    }
    $name = $path . '/' . $date . '/' . $CONCESS . ' - ' . $y . '_' . $m . ' - ' . $sep . '.xlsx';

    $subject = $CONCESS . ' - ' . $y . '_' . $m . ' - ' . $sep;
    $subject2 = utf8_decode('Implantação Claro - ') . $subject;

    if (!file_exists($name)) {
        $name = $path . '/' . $date . '/' . $CONCESS . ' - ' . $y . '_' . $m . ' - ' . $sep . '.xlsx';
        $tname = $name;
    } else {
        $name = $path . '/' . $date . '/' . $datetime . ' ' . $CONCESS . ' - ' . $y . '_' . $m . ' - ' . $sep . '.xlsx';
        $temp = $path . '/TEMP' . '/' . $date;
        if (!file_exists($temp)) {
            mkdir($temp, 0777, true);
        }
        $tname = $temp . '/' . $CONCESS . ' - ' . $y . '_' . $m . ' - ' . $sep . '.xlsx';
        $twriter = new Xlsx($spreadsheetxlx);
        $twriter->save($tname);
    }
    $emailFile = $tname;

    $writer = new Xlsx($spreadsheetxlx);
    $writer->save($name);
    if ($writer) {
        $message = utf8_decode('Relatório salvo com sucesso!');
        ?>
        <script>
            var encoding = document.characterSet;
            if (encoding == 'UTF-8') {
                alert('Relatório salvo com sucesso!');
            }else{
                alert('<?=$message?>');
            }
        </script>
        <?php
}
    if (!isset($sendmail)) {
        $sendmail = false;
    }
    if ($printxls !== true || $sendmail == true) {
        $mail = new PHPMailer();
//Descomentar para realizar o debug em caso de erros
        // $mail->SMTPDebug = 1;
        // $mail->Debugoutput = 'html';
        $mail->setLanguage('pt');
        $mail->Encoding = 'base64';

//Configurações do e-mail
        $mail->isSMTP();
        $mail->Host = HOST;
        $mail->AuthType = 'LOGIN';
        $mail->SMTPAuth = true;
        $mail->SMTPSecure = 'ssl';
        $mail->Username = EMAIL;
        $mail->Password = PASS;
        $mail->Port = PORT;

//Insere o remetente
        $mail->setFrom(EMAIL, NOME, 0);

//Destinatários
        $mail->addAddress(EMAIL);
        $mail->addAddress(DEST);

//Habilita HTML e instância o corpo do e-mail
        $mail->isHTML(true);
        $mail->Subject = $subject2;
        $mail->Body = ($html);
        $mail->AddAttachment($emailFile);

        if (!$mail->send()) {
            echo 'Não foi possível enviar a mensagem.<br>';
            echo 'Erro: ' . $mail->ErrorInfo;
        } else {
            if (is_dir("$path/TEMP/")) {
                array_map('unlink', glob("$path/TEMP/*/*"));
                array_map('rmdir', glob("$path/TEMP/*"));
                array_map('rmdir', glob("$path/TEMP/"));
            }
            $message2 = utf8_decode('E-mail enviado com sucesso!');
            // echo 'E-mail enviado com sucesso!'<br>';
            echo "<script>";
            echo "alert('$message2')";
            echo "</script>";
        }

    }
//
}
