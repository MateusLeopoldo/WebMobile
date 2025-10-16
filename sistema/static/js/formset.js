document.addEventListener('DOMContentLoaded', function() {
    const addFormBtn = document.getElementById('add-form');
    const formList = document.getElementById('musicas-form-list');
    const emptyForm = document.getElementById('empty-form').innerHTML;
    const totalForms = document.getElementById('id_musica_set-TOTAL_FORMS');

    addFormBtn.addEventListener('click', function() {
        let currentFormCount = formList.children.length;
        let newForm = emptyForm.replace(/__prefix__/g, currentFormCount);
        
        let newFormDiv = document.createElement('div');
        newFormDiv.className = 'musica-form';
        newFormDiv.innerHTML = newForm;
        
        formList.appendChild(newFormDiv);
        totalForms.value = currentFormCount + 1;
    });
});