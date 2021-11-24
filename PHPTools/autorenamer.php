<?php
if (!isset($test)) {
    $test = 0;
}
// $test = 1;
if (isset($_POST["insere"]) && $_POST["insere"] != "" || $test == 1) {
//AUTO RENAME
    //VERIFICA SE .PDF
    if (isset($filename)) {
    /**
        Encoding table
     *  Amazonas-1-wonder
     *      Sem encoding
     *  LIGHT
     *      Sem encoding
     *  CPFL
     *      $file = $arquivo
     *  Enegisa-PB
     *      Sem encoding
     *  CEB
     *      Sem encoding
     *  Eletropaulo
     *      Sem encoding
     *  Cosern
     *      Sem encoding
     *  Copel
     *      Sem encoding
     * 
     * 
     */
       $file =  utf8_decode($filename);
    }
    if (isset($fat->unidade)) {
        $uc = $fat->unidade;
    }
    if (isset($fat->mesRef)) {
        $mes_ref = $fat->mesRef;
    }
    if (strpos($file, '.csv')) {
        $file = str_replace('.csv','.pdf',$file);
    }
    if (strpos($file, '.xlsx')) {
        $file = str_replace('.xlsx','.pdf',$file);
    }
    if (isset($fat->valid)) {
        $valid = $fat->valid;
    }
    //VERIFICA PROCEDURAL
    if (isset($valid)) {
        //DEFINE PASTA CONVERSAO E ARQUIVOS $FILE
        $path = "$localArquivos\\$file";
        if (!file_exists($path)) {
            if (!strpos($localArquivos,"Conversao2")) {
                $localArquivos = str_replace('Conversao','Conversao2',$localArquivos);
                $path = "$localArquivos\\$file";
            }
        }
        //VERIFICA FATURA VALIDA
        if ($valid) {
            //CRIA MESREF
            $mes_formatado = DateTime::createFromFormat('Y-m-d', $mes_ref);
            $mes_formatado = $mes_formatado->format('Y-m-d');
            //CRIA PASTA MESREF EM UPLOADFATURAS
            $newpath = UPLOAD."$mes_formatado\\";
            if (!file_exists($newpath)) {
                mkdir($newpath, 0777, true);
            }
            //CRIA PASTA MESREF EM CONVERSAO
            $newpath2 = "$localArquivos\Renomeadas\\$mes_formatado\\";
            if (!file_exists($newpath2)) {
                mkdir($newpath2, 0777, true);
            }
            //DEFINE NOVO NOME
            $newfile = "$newpath$uc.pdf";
            $newfile2 = "$newpath2$uc.pdf";
            //COPIA ARQUIVO DE CONVERSAO PARA UPLOADFATURAS
            if (!copy($path, $newfile)) {
                echo "Erro ao copiar arquivo $path para $newpath <br>";
            }else{
                echo "Arquivo $file copiado para Arquivos!<br>";
            }
            if (!copy($path, $newfile2)) {
                echo "Erro ao copiar arquivo $path para $newpath2 <br>";
            }else{
                // echo "Arquivo $file copiado para Renomeados!<br>";
            }
        //VERIFICA FATURA INVALIDA
        } elseif (!$valid) {
            /**
            TABELA CASOS RENAME
             */
            $textfound = '';
            ####### REATIVO ########
            if (strpos($erro,'Reativo') !== false) {
                $textfound = 'Reativo';
            }
            if (isset($fat->erro) && strpos($fat->erro,'Reativo') !== false) {
                $textfound = 'Reativo';
            }
            ####### MEDIA ########
            if (strpos($erro,'Media') !== false || strpos($erro,'MT') !== false || strpos($erro,'média') !== false) {
                $textfound = 'MT';
            }
            if (isset($fat->erro) && strpos($erro,'Media') !== false || strpos($erro,'MT') !== false) {
                $textfound = 'MT';
            }
            ####### IMPLANTADA ########
            if (strpos($erro,'cadastrada') !== false) {
                $textfound = 'Implantada';
            }
            if (isset($fat->erro) &&strpos($fat->erro,'cadastrada') !== false) {
                $textfound = 'Implantada';
            }
            ####### PERDAS ########
            if (strpos($erro,'perdas') !== false) {
                $textfound = 'Perdas';
            }
            if (isset($fat->erro) && strpos($fat->erro,'perdas') !== false) {
                $textfound = 'Perdas';
            }
            ####### SUBSIDIO ########
            if (strpos($erro,'subsidio') !== false) {
                $textfound = 'Subsidio';
            }
            if (isset($fat->erro) && strpos($fat->erro,'subsidio') !== false) {
                $textfound = 'Subsidio';
            }
            /**
             * CASES DO SWITCH $textfound
             */
            switch($textfound){
                case 'Reativo':
                    $foldername  = 'Reativo';
                    $newpath = "$localArquivos\\Nao Implantadas\\Reativo\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
                case 'Implantada':
                    $foldername  = 'Implantada';
                    $newpath = "$localArquivos\\Nao Implantadas\\Implantada\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
                case 'MT':
                    $foldername  = 'Media Tensao';
                    $newpath = "$localArquivos\\Nao Implantadas\\Media Tensao\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
                case 'Perdas':
                    $foldername  = 'Perdas';
                    $newpath = "$localArquivos\\Nao Implantadas\\Perdas\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
                case 'Subsidio':
                    $foldername  = 'Subsidio';
                    $newpath = "$localArquivos\\Nao Implantadas\\Subsidio\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
                default:
                    $foldername  = 'N Implantada';
                    $newpath = "$localArquivos\\Nao Implantadas\\";
                    if (!file_exists($newpath)) {
                        mkdir($newpath, 0777, true);
                    }
                    break;
            }
            //DEFINE ARQUIVO E COPIA
            $newfile = "$newpath$uc.pdf";
            if (!copy($path, $newfile)) {
                echo "Erro ao copiar arquivo $path <br>";
            }else{
                echo "Arquivo $file copiado para $foldername!<br>";
            }
        }
    }
}
//
