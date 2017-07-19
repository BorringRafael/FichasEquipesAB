$(document).ready(function() {

  var codeEstado;
  var codeMunicipio;
  var codeEstabelecimento;


  $("#estados").change(function () {
      var codeEstado = $( this ).val();
      $.getJSON("/esus/busca", {municipios: codeEstado}, function(data) {
        $('#municipios').empty();
        $('#estabelecimentos').empty();
        $('#equipes').empty();
        $('#municipios').append(new Option("", ""));
        $.each(data, function(k, v) {
            $('#municipios').append(new Option(v, k));
        });
      });
    });

  $("#municipios").change(function () {
      var codeMunicipio = $( this ).val();
      $.getJSON("/esus/busca", {estabelecimentos: codeMunicipio}, function(data) {
        $('#estabelecimentos').empty();
        $('#equipes').empty();
        $('#estabelecimentos').append(new Option("", ""));
        $.each(data, function(k, v) {
          if (v.natJuridica == 1) {
            $('#estabelecimentos').append(new Option(v.noFantasia, v.id));
          };
        });
      });
    });

  $("#estabelecimentos").change(function () {
      var codeEstabelecimento = $( this ).val();
      $.getJSON("/esus/busca", {equipes: codeEstabelecimento}, function(data) {
        $('#equipes').empty();
        $('#equipes').append(new Option("", ""));
        $.each(data, function(k, v) {
          $('#equipes').append(new Option(v.coArea + " - " + v.nomeEquipe, codeEstabelecimento + "|" + codeEstabelecimento.substring(0, 6) + "|" + v.coArea + "|" + v.tpEquipe));
        });
      });
    });

  $("#equipes").change(function () {
      var code = $( this ).val().split("|");
      $.getJSON("/esus/busca", {profissionais: code[0], municipioss: code[1], area: code[2], tipo: code[3]}, function(data) {
        $('#profissionais').empty();
        $('#profissionais').append(new Option("", ""));
        $.each(data, function(k, v) {
          $('#profissionais').append(new Option(v.noProfissional + " - " + v.dsCbo, v.cns));
        });
      });
    });
});
