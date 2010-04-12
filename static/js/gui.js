var Taskr = {};
Taskr.gui = {};
Taskr.gui.showError = function(message){
    $("#errors").html(message);
};

Taskr.gui.onErrorClick = function(){
    $("#errors").html("");
};

Taskr.gui.showMessage = function(message){
    $("#messages").html(message);
};

Taskr.gui.onMessageClick = function(){
    $("#messages").html("");
};

Taskr.gui.showByPriority = function(priority){
    requests.taskByPriority(priority, Taskr.gui.onShowByPriorityOK,
            Taskr.gui.onShowByPriorityError);
    return false;
};

Taskr.gui.onShowByPriorityOK = function(response){
    Taskr.gui.fillTasks(response, true);
};

Taskr.gui.onShowByPriorityError = function(response){
    Taskr.gui.showError("Tasks load failed " + response.responseText);
};

Taskr.gui.onCreateTask = function(){
    var name, desc, priority, date, time, timestamp, tags, task;
    name = $("#taskname").val().trim();
    desc = $("#taskdesc").val().trim();
    priority = $("#taskprio").val();
    date = $('#taskdate').datepicker("getDate");
    time = $('#taskhour').timeEntry("getTime");

    date.setHours(time.getHours());
    date.setMinutes(time.getMinutes());

    tags = Taskr.tagsFromString($("#tasktags").val());

    if(name === "") {
        Taskr.gui.showError("Empty name");
        return;
    }
    else if(timestamp < (new Date).getTime()) {
        Taskr.gui.showError("End date is in the past");
        return;
    }

    timestamp = date.getTime() / 1000;

    task = Taskr.Task(name, desc, timestamp, priority, false, null, tags);
    requests.createTask(task, Taskr.gui.onCreateTaskOK,
            Taskr.gui.onCreateTaskError);
};

Taskr.gui.onCreateTaskOK = function(response) {
    Taskr.gui.showMessage("Task created");
    $("#taskname").val("");
    $("#taskdesc").val("");
    Taskr.gui.loadTags();
    Taskr.gui.loadTasks();
};

Taskr.gui.onCreateTaskError = function(response) {
    Taskr.gui.showError("Task creation failed " + response.responseText);
};

Taskr.gui.loadTags = function(){
    requests.getTags(Taskr.gui.loadTagsOK, Taskr.gui.loadTagsError);
};

Taskr.gui.loadTagsOK = function(data){
    Taskr.gui.fillTags(data, true);
    return false;
};

Taskr.gui.fillTags = function(tags, clean){
    var index, tag, cont;
    cont = $("#tags");

    if(clean){
        cont.html("");
    }

    for(index in tags){
        tag = tags[index];
        cont.append(Taskr.formatTag(tag));
    }
};

Taskr.gui.loadTagsError = function(data){
    Taskr.gui.showError("Tags failed to load: " + data.responseText);
};

Taskr.gui.showTasksByTag = function(tag){
    requests.taskByTag(tag, Taskr.gui.onShowTasksByTagOK,
            Taskr.gui.onShowTasksByTagError);
    return false;
};

Taskr.gui.onShowTasksByTagOK = function(tasks){
    Taskr.gui.fillTasks(tasks, true);
};

Taskr.gui.onShowTasksByTagError = function(response){
    Taskr.gui.showError("Tasks failed to load: " + response.responseText);
};

Taskr.gui.loadTasks = function(){
    requests.getTasks(Taskr.gui.loadTasksOK, Taskr.gui.loadTasksError);
    return false;
};

Taskr.gui.loadTasksOK = function(data){
    Taskr.gui.fillTasks(data, true);
    return false;
};

Taskr.gui.fillTasks = function(tasks, clean){
    var index, task, cont, content;
    cont = $("#tasks");

    if(clean){
        cont.html("");
    }

    for(index in tasks){
        task = tasks[index];
        // XXX: esto no se hace
        content = $('<div class="task priority-' + task.priority + '" id="task-' + task.identifier + '"><div class="tag-desc"><input type="checkbox" onclick="Taskr.gui.onTaskFinish(' + task.identifier + ');" /><sub>' + Taskr.gui.formatDate(task.end) + '</sub> <strong>' + task.name + '</strong> <em>' + task.description + '</em></div><div class="tags-by-task">' + Taskr.printTagsByTask(task)  + '</div></div>');

        if(task.finished){
            content.css('text-decoration', 'line-through').removeClass('priority-' + task.priority);
            $('input', content).attr('checked', 'true').attr('disabled', 'true');
        }

        content.data('task', task);
        cont.append(content);
    }
};

Taskr.gui.onTaskFinish = function(identifier){
    var task = $('#task-' + identifier).data('task');
    task.finished = true;
    requests.modifyTask(task,
            function(response){Taskr.gui.onTaskFinishOK(response, task);},
            Taskr.gui.onTaskFinishError);
};

Taskr.gui.onTaskFinishOK = function(response, task){
    console.log(response);
    $('#task-' + task.identifier).css('text-decoration', 'line-through').removeClass('priority-' + task.priority);
    $('#task-' + task.identifier + ' input').attr('disabled', 'true');
};

Taskr.gui.onTaskFinishError = function(response){
    Taskr.gui.showError("Tasks update failed: " + response.responseText);
};

Taskr.gui.formatDate = function(timestamp){
    date = (new Date(timestamp * 1000));
    return date.toLocaleDateString() + " " + date.toLocaleTimeString();
};

Taskr.formatTag = function(tag){
    // XXX: esto no se hace
    return '<a href="#" class="tag" onclick="return Taskr.gui.showTasksByTag(\'' + tag.name + '\');">' + tag.name + '</a>';
};

Taskr.printTagsByTask = function(task){
    var result = "", tag;
    for(index in task.tags){
        tag = task.tags[index];
        result += Taskr.formatTag(tag);
    }

    return result;
};

Taskr.gui.loadTasksError = function(data){
    Taskr.gui.showError("Tasks failed to load: " + data.responseText);
};
