<?php
//MEIO XLS
use PhpOffice\PhpSpreadsheet\Style\Border;
use PhpOffice\PhpSpreadsheet\Style\Fill;

//Fix de char especial em nome do arquivo

if (isset($filename)) {
    $file = $filename;
}
//DEFINIÇÕES DE ESTILOS DAS CELLS
//VARIAVEL $VALID
if ($valid) {
    $styleArray = array(
        'fill' => array(
            'fillType' => Fill::FILL_SOLID,
            'startColor' => array('argb' => 'D0E9C6'),
        ),
        'borders' => array(
            'outline' => array(
                'borderStyle' => Border::BORDER_THICK,
                'color' => array('rgb' => 'DDDDDD'),
            ),
        ),
    );
}
if (!$valid) {
    $styleArray = array(
        'fill' => array(
            'fillType' => Fill::FILL_SOLID,
            'startColor' => array('argb' => 'F2DEDE'),
        ),
        'borders' => array(
            'outline' => array(
                'borderStyle' => Border::BORDER_THICK,
                'color' => array('rgb' => 'DDDDDD'),
            ),
        ),
    );
}

//VARIAVEL $FAT->VALID
if (isset($fat->valid)) {
    if($fat->valid){
        $styleArray = array(
            'fill' => array(
                'fillType' => Fill::FILL_SOLID,
                'startColor' => array('argb' => 'D0E9C6'),
            ),
            'borders' => array(
                'outline' => array(
                    'borderStyle' => Border::BORDER_THICK,
                    'color' => array('rgb' => 'DDDDDD'),
                ),
            ),
        );
    }

    if (!$fat->valid) {
        $styleArray = array(
            'fill' => array(
                'fillType' => Fill::FILL_SOLID,
                'startColor' => array('argb' => 'F2DEDE'),
            ),
            'borders' => array(
                'outline' => array(
                    'borderStyle' => Border::BORDER_THICK,
                    'color' => array('rgb' => 'DDDDDD'),
                ),
            ),
        );
    }
    //ENTITY DECODE ORIENTADO A OBJETO
    $fat->erro = html_entity_decode($fat->erro);
    $fat->ocorrencia = html_entity_decode($fat->ocorrencia);
    if (isset($Nome_Empresa)) {
        $Nome_Empresa = html_entity_decode($Nome_Empresa);
    }
    if (isset($nome_empresa)) {
        $nome_empresa = html_entity_decode($nome_empresa);
    }
    
//INICIO XLSX ORIENTADO A OBJETO
    //CASO SE FATURA FOR INVALIDA
    if (isset($fat->valid)) {
    if ($fat->valid == false) {
        $contxls++;
        $sheet->setCellValue('A' . ($contxls + 1), $file);
        $sheet->getStyle('A' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('B' . ($contxls + 1), $fat->unidade);
        $sheet->getStyle('B' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('C' . ($contxls + 1), $fat->erro);
        $sheet->getStyle('C' . ($contxls + 1))->applyFromArray($styleArray);
        for ($i = 'D'; $i !== 'AB'; $i++) {
            $sheet->getStyle($i . ($contxls + 1))->applyFromArray($styleArray);
        }
    } else {
    //CASO SE FATURA FOR VALIDA
        $contxls++;
        $sheet->setCellValue('A' . ($contxls + 1), $file);
        $sheet->getStyle('A' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('B' . ($contxls + 1), $fat->unidade);
        $sheet->getStyle('B' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('C' . ($contxls + 1), $erro);
        $sheet->getStyle('C' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('D' . ($contxls + 1), $retorno["Dif_Achado"]);
        $sheet->getStyle('D' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->getStyle('D' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->setCellValue('E' . ($contxls + 1), $retorno['DescontoBase']);
        $sheet->getStyle('E' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->getStyle('E' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->setCellValue('F' . ($contxls + 1), $retorno['Outros_Base']);
        $sheet->getStyle('F' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->getStyle('F' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('G' . ($contxls + 1), $fat->mesRef);
        $sheet->getStyle('G' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('H' . ($contxls + 1), $fat->diasFatura);
        $sheet->getStyle('H' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('I' . ($contxls + 1), $fat->dataEmissao);
        $sheet->getStyle('I' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('J' . ($contxls + 1), Formata_Dinheiro($fat->totalFaturado));
        $sheet->getStyle('J' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('K' . ($contxls + 1), Formata_Dinheiro($fat->totalCalculado));
        $sheet->getStyle('K' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('L' . ($contxls + 1), $fat->consumo);
        $sheet->getStyle('L' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('M' . ($contxls + 1), $KWH_FP_Ind_Fat_R);
        $sheet->getStyle('M' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('N' . ($contxls + 1), $fat->consumo_injetado);
        $sheet->getStyle('N' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('O' . ($contxls + 1), $custoDisp_Reais);
        $sheet->getStyle('O' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($saldo_mes_total_fat)) {
            $sheet->setCellValue('P' . ($contxls + 1), $saldo_mes_total_fat);
        } else {
            $sheet->setCellValue('P' . ($contxls + 1), '0');
        }
        $sheet->getStyle('P' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Q' . ($contxls + 1), Formata_Dinheiro($fat->devolucao));
        $sheet->getStyle('Q' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('R' . ($contxls + 1), Formata_Dinheiro($fat->outros));
        $sheet->getStyle('R' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('S' . ($contxls + 1), Formata_Dinheiro($fat->duplicidade));
        $sheet->getStyle('S' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('T' . ($contxls + 1), Formata_Dinheiro($fat->creditoValor));
        $sheet->getStyle('T' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('U' . ($contxls + 1), $fat->notaFiscal);
        $sheet->getStyle('U' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('V' . ($contxls + 1), $fat->medidor);
        $sheet->getStyle('V' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($proc_judicial)) {
            $sheet->setCellValue('W' . ($contxls + 1), $proc_judicial);
        } else {
            $sheet->setCellValue('W' . ($contxls + 1), '');
        }
        $sheet->getStyle('W' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('X' . ($contxls + 1), $fat->ocorrencia);
        $sheet->getStyle('X' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Y' . ($contxls + 1), $Perdas);
        $sheet->getStyle('Y' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Z' . ($contxls + 1), $fat->cnpj);
        $sheet->getStyle('Z' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($Nome_Empresa)) {
            $sheet->setCellValue('AA' . ($contxls + 1), $Nome_Empresa);
        }
        if (isset($nome_empresa)) {
            $sheet->setCellValue('AA' . ($contxls + 1), $nome_empresa);
        }
        $sheet->getStyle('AA' . ($contxls + 1))->applyFromArray($styleArray);
    //SETANDO VARIAVEIS PARA fimxls.php
    $cod_usuario = $codUsuario;
    $maior_dif = $maiorDiferenca;
    $menor_dif = $menorDiferenca;
    $tot_dif_achado = $totalComDiferenca;
    $fat_exist_geral = $fatsJaCadastradas;
    $total_nao_existe = $unidadeNaoExiste;
    $fat_novas_geral = $fatsInseridas;
    $total_nao_inserida = $totalNaoInseridas;
    $mes_ref = $fat->mesRef;
    //CONCESSIONARIAS
        if($codConcess == 48) {
            $CONCESS = 'ELETROBRAS RORAIMA - BOA VISTA';
        }
        if ($codConcess == 40) {
            $CONCESS = 'ELETROBRAS AMAZONAS';
        }
        if ($codConcess == 19) {
            $CONCESS = 'CERON ELETROBRAS RONDONIA';
        }
        if ($codConcess == 46) {
            $CONCESS = 'CEPISA ELETROBRAS PIAUI';
        }
        if ($codConcess == 33) {
            $CONCESS = 'CEAL';
        }
        if ($codConcess == 50) {
            $CONCESS = 'CEA';
        }
        if ($codConcess == 49) {
            $CONCESS = 'ELETROACRE (Energisa Acre)';
        }

    }
}
//FIM VERSÃO XLSX ORIENTADO A OBJETO $FAT
}else{
//INICIO VERSÃO XLSX PROCEDURAL
    $erro = html_entity_decode($erro);
    $obs = html_entity_decode($obs);
    if (isset($Nome_Empresa)) {
        $Nome_Empresa = html_entity_decode($Nome_Empresa);
    }
    if (isset($nome_empresa)) {
    $nome_empresa = html_entity_decode($nome_empresa);
    }
    if ($valid == false) {
        $contxls++;
        $sheet->setCellValue('A' . ($contxls + 1), $file);
        $sheet->getStyle('A' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('B' . ($contxls + 1), $uc);
        $sheet->getStyle('B' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('C' . ($contxls + 1), $erro);
        $sheet->getStyle('C' . ($contxls + 1))->applyFromArray($styleArray);
        for ($i = 'D'; $i !== 'AB'; $i++) {
            $sheet->getStyle($i . ($contxls + 1))->applyFromArray($styleArray);
        }
    } else {
        $contxls++;
       // echo $file;
        $sheet->setCellValue('A' . ($contxls + 1), $file);
        $sheet->getStyle('A' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('B' . ($contxls + 1), $uc);
        $sheet->getStyle('B' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('C' . ($contxls + 1), $erro);
        $sheet->getStyle('C' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('D' . ($contxls + 1), $retorno["Dif_Achado"]);
        $sheet->getStyle('D' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->getStyle('D' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->setCellValue('E' . ($contxls + 1), $retorno['DescontoBase']);
        $sheet->getStyle('E' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->getStyle('E' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->setCellValue('F' . ($contxls + 1), $retorno['Outros_Base']);
        $sheet->getStyle('F' . ($contxls + 1))->getFont()->getColor()->setRGB('FF0000');
        $sheet->getStyle('F' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('G' . ($contxls + 1), $mes_ref);
        $sheet->getStyle('G' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('H' . ($contxls + 1), $dias_fat);
        $sheet->getStyle('H' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('I' . ($contxls + 1), $data_emissao);
        $sheet->getStyle('I' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('J' . ($contxls + 1), Formata_Dinheiro($Total_Fatura));
        $sheet->getStyle('J' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('K' . ($contxls + 1), Formata_Dinheiro($Total_Achado));
        $sheet->getStyle('K' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('L' . ($contxls + 1), $KWH_FP_Ind_Reg);
        $sheet->getStyle('L' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('M' . ($contxls + 1), $KWH_FP_Ind_Fat_R);
        $sheet->getStyle('M' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('N' . ($contxls + 1), $consumo_injetado);
        $sheet->getStyle('N' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('O' . ($contxls + 1), $custodisp_fat_r);
        $sheet->getStyle('O' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($saldo_injetada_fatura)) {
            $sheet->setCellValue('P' . ($contxls + 1), $saldo_injetada_fatura);
        } else {
            $sheet->setCellValue('P' . ($contxls + 1), '0');
        }
        $sheet->getStyle('P' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Q' . ($contxls + 1), Formata_Dinheiro($dev));
        $sheet->getStyle('Q' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('R' . ($contxls + 1), Formata_Dinheiro($Outros));
        $sheet->getStyle('R' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($duplicidade)) {
            $sheet->setCellValue('S' . ($contxls + 1), Formata_Dinheiro($duplicidade));
        }
        $sheet->getStyle('S' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('T' . ($contxls + 1), Formata_Dinheiro($CreditoValor));
        $sheet->getStyle('T' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('U' . ($contxls + 1), $nf);
        $sheet->getStyle('U' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('V' . ($contxls + 1), $medidor);
        $sheet->getStyle('V' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($proc_judicial)) {
            $sheet->setCellValue('W' . ($contxls + 1), $proc_judicial);
        } else {
            $sheet->setCellValue('W' . ($contxls + 1), '');
        }

        $sheet->getStyle('W' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('X' . ($contxls + 1), $obs);
        $sheet->getStyle('X' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Y' . ($contxls + 1), $Perdas);
        $sheet->getStyle('Y' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->setCellValue('Z' . ($contxls + 1), $CNPJ);
        $sheet->getStyle('Z' . ($contxls + 1))->applyFromArray($styleArray);
        if (isset($Nome_Empresa)) {
            $sheet->setCellValue('AA' . ($contxls + 1), $Nome_Empresa);
        }
        if (isset($nome_empresa)) {
            $sheet->setCellValue('AA' . ($contxls + 1), $nome_empresa);
        }
        $sheet->getStyle('AA' . ($contxls + 1))->applyFromArray($styleArray);
        $sheet->getStyle('AA' . ($contxls + 1))->applyFromArray($styleArray);
    }
    //FIM XLSX PROCEDURAL
}
