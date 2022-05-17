<?php

include("config.php");


$limit = 10;

if(isset($_GET["n"]) && settype($_GET["n"],"integer") ){
	$limit = $_GET["n"];
}

try {
    $base_de_datos = new PDO("pgsql:host=$host;port=5432;dbname=$db", $user, $password);
    $base_de_datos->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	$sql = 'SELECT * FROM predictions where prediction_result is not null order by id DESC limit '.$limit;

	$linea = "";

    foreach ($base_de_datos->query($sql) as $row) {

    	$tmp_local = $row["local"];
    	$tmp_local_gf = $row["local_goles"];
    	$tmp_local_gc = $row["local_goles_recibidos"];
    	$tmp_local_df = $row["local_dif_goles"];
    	$tmp_local_matches = $row["local_jornadas_jugadas"];

		$tmp_visita = $row["visita"];
    	$tmp_visita_gf = $row["visita_goles"];
    	$tmp_visita_gc = $row["visita_goles_recibidos"];
    	$tmp_visita_df = $row["visita_dif_goles"];
    	$tmp_visita_matches = $row["visita_jornadas_jugadas"];

    	$ganador = $row["prediction_result"];



        $linea .= "<tr onclick=createChar('".rawurlencode($tmp_local)."',".$tmp_local_gf.",".$tmp_local_gc.",".$tmp_local_df.",".$tmp_local_matches.",'".rawurlencode($tmp_visita)."',".$tmp_visita_gf.",".$tmp_visita_gc.",".$tmp_visita_df.",".$tmp_visita_matches.",'".$ganador."') ><td>".$tmp_local."</td><td>".$tmp_local_gf."</td><td>".$tmp_local_gc."</td><td>".$tmp_local_df."</td><td>".$tmp_local_matches."</td><td>".$tmp_visita."</td><td>".$tmp_visita_gf."</td><td>".$tmp_visita_gc."</td><td>".$tmp_visita_df."</td><td>".$tmp_visita_matches."</td><td>".$ganador."</td></tr>";
    }


} catch (Exception $e) {
    echo "Ocurrió un error con la base de datos: " . $e->getMessage();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>

	<title>Easy money betting system</title>
	<!-- CSS only -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
	<!-- JavaScript Bundle with Popper -->
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
</head>
<body>
	<nav class="navbar navbar-expand-lg bg-light">
	  <div class="container-fluid">
	  	<img src="logo-arq.jpeg" style="max-height: 50px; width: auto;">
	    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
	      <span class="navbar-toggler-icon"></span>
	    </button>
	    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
	      <div class="navbar-nav">
	        <a class="nav-link active" aria-current="page" href="https://github.com/FabianOrduna/cuddly-broccoli" target="_blank">Github Repo</a>
	        <a class="nav-link" href="https://github.com/FabianOrduna/cuddly-broccoli/tree/main/Dags" target="_blank">Dags</a>
	        <a class="nav-link" href="https://github.com/FabianOrduna/cuddly-broccoli/tree/main/model" target="_blank">Model</a>
	      </div>
	    </div>
	  </div>
	</nav>
	<div class="container">
		<div class="row mt-5">
			<div class="col-md-8">
					<table class="table table-striped">
						<thead>
						    <tr>
						      <th scope="col">Local</th>
						      <th scope="col">GF</th>
						      <th scope="col">GC</th>
						      <th scope="col">DG</th>
						      <th scope="col">Match #</th>
						      <th scope="col">Visita</th>
						      <th scope="col">GF</th>
						      <th scope="col">GC</th>
						      <th scope="col">DG</th>
						      <th scope="col">Match #</th>
						      <th scope="col">PREDICTION</th>
						    </tr>
						</thead>
						<tbody>
							<?php print $linea; ?>	
						</tbody>
					</table>
			</div>
			<div class="col-md-4">
				<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.min.js" integrity="sha512-QSkVNOCYLtj73J4hbmVoOV6KVZuMluZlioC+trLpewV8qMjsWqlIQvkn1KGX2StWvPMdWGBqim1xlC8krl1EKQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

				<div>
				  <canvas id="myChart" height="250px" style="display: none;"></canvas>
				  <p id="label-result" style="display: none;" class="text-center">Resultado: <b id="predicted_result"></b></p>
				</div>

				<img src="https://www.api-football.com/public/img/home1/hero-banner.png" class="img-fluid">

			</div>
		</div>
	</div>

	<script type="text/javascript">

		theChar = null;
		
		function createChar(local,local_gf, local_gc, local_dg, local_matches, visita, visita_gf, visita_gc, visita_dg, visita_matches, ganador){

			document.getElementById('myChart').style.display = "";

			if(theChar!=null){
				theChar.destroy();
			}

			local = decodeURI(local);
			visita = decodeURI(visita);

			const labels = [
			    'GF',
			    'GC',
			    'DG',
			    '#Matchs'
			  ];

			const data = {
			  labels: labels,
			  datasets: [
			    {
			      label:  local,
			      data: [local_gf,local_gc,local_dg, local_matches],
			      backgroundColor: "#aed581",
			    },
			    {
			      label:  visita,
			      data: [visita_gf,visita_gc,visita_dg, visita_matches],
			      backgroundColor: "#ffe082",
			    }
			  ]
			};

			const config = {
			  type: 'bar',
			  data: data,
			  options: {
			    responsive: true,
			    plugins: {
			      legend: {
			        position: 'top',
			      },
			      title: {
			        display: true,
			        text: 'Premier league: '+local+' vs. '+visita+''
			      }
			    }
			  },
			};

			theChar = new Chart(document.getElementById('myChart'),config);
			
			document.getElementById("label-result").style.display = "";
			document.getElementById("predicted_result").innerHTML = ganador;
		}

	</script>

</body>
</html>
