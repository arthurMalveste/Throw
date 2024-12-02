document.getElementById('bug-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const nome = event.target.nome.value;
    const email = event.target.email.value;
    const mensagem = event.target.mensagem.value;

    // Referência ao Realtime Database
    const bugReportRef = firebase.database().ref('bugReports');

    // Criar um novo ID para o relatório de bug
    const novoBugReport = bugReportRef.push();

    // Salvar os dados no Realtime Database
    novoBugReport.set({
        nome: nome,
        email: email,
        mensagem: mensagem,
        data: new Date().toISOString()
    }).then(() => {
        alert('Bug reportado com sucesso!');

        // Limpar o formulário
        event.target.reset();
    }).catch((error) => {
        alert('Erro ao enviar o bug: ' + error.message);
    });
});
