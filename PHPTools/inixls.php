<?php
$contxls = 0;
include './SYSTOOLS/vendor/autoload.php';
use PhpOffice\PhpSpreadsheet\Spreadsheet;
$spreadsheetxlx = new Spreadsheet();
$sheet = $spreadsheetxlx->getActiveSheet();
$sheet->setCellValue('A' . ($contxls + 1), "Arquivo");
$sheet->setCellValue('B' . ($contxls + 1), "Unidade");
$sheet->setCellValue('C' . ($contxls + 1), "Erro");
$sheet->setCellValue('D' . ($contxls + 1), "Diferença achada");
$sheet->setCellValue('E' . ($contxls + 1), "Desconto Base");
$sheet->setCellValue('F' . ($contxls + 1), "Outros Base");
$sheet->setCellValue('G' . ($contxls + 1), "Mes Referencia");
$sheet->setCellValue('H' . ($contxls + 1), "Dias da Fatura");
$sheet->setCellValue('I' . ($contxls + 1), "Data de Emissao");
$sheet->setCellValue('J' . ($contxls + 1), "Total Fatura");
$sheet->setCellValue('K' . ($contxls + 1), "Total Achado");
$sheet->setCellValue('L' . ($contxls + 1), "Consumo Total");
$sheet->setCellValue('M' . ($contxls + 1), "Consumo + Perdas");
$sheet->setCellValue('N' . ($contxls + 1), "Consumo Injetado");
$sheet->setCellValue('O' . ($contxls + 1), "Custo Disp Energia Injetada");
$sheet->setCellValue('P' . ($contxls + 1), "Saldo Informado na Fatura");
$sheet->setCellValue('Q' . ($contxls + 1), "Devoluçao");
$sheet->setCellValue('R' . ($contxls + 1), "Outros");
$sheet->setCellValue('S' . ($contxls + 1), "Duplicidade");
$sheet->setCellValue('T' . ($contxls + 1), "Credito Prox. Ciclo");
$sheet->setCellValue('U' . ($contxls + 1), "Nota Fiscal");
$sheet->setCellValue('V' . ($contxls + 1), "Medidor");
$sheet->setCellValue('W' . ($contxls + 1), "Processo Judicial");
$sheet->setCellValue('X' . ($contxls + 1), "Ocorrencia");
$sheet->setCellValue('Y' . ($contxls + 1), "Perdas");
$sheet->setCellValue('Z' . ($contxls + 1), "CNPJ");
$sheet->setCellValue('AA' . ($contxls + 1), "Nome Empresa");
$separacao = false;
if (isset($_POST["separacao"])) {
    $separacao = $_POST["separacao"];
}
