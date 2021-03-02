var conveyor_form_class_name = '.js-conveyor-form';
var vertex_api_url = $(conveyor_form_class_name).attr('vertices-url')
var datavariable_api_url = $(conveyor_form_class_name).attr('datavariables-url')
    
// Create graph container
var $flowchart = $('#conveyor-workspace');

var datavariableOptions = {
    sDom: 'tr',
    paginate: false,
    scrollY: 165,
    autoWidth: false,
    deferRender: true,
    select: {
        style: 'single',
    },
    columns: [
        { 'data': 'id' },
        { 'data': 'label' },
    ],
    columnDefs: [
        { width: '20%', targets: 0 },  // Id
        { width: '80%', targets: 1 },  // Computing mocule
    ],    
};

var makeListItem = function(id, moduleName, conditionOption, conditionValue) {
    var classes = "list-group-item js-add-element-button";
    var condition = '';
    if (conditionValue != '-') {
        condition = `[if ${conditionOption}=${conditionValue}]`
    };
    var listItem = $(
    `<a href="#" class="${classes}" value="${id}"
        module-name="${moduleName}"
        condition-option="${conditionOption}"
        condition-value="${conditionValue}">
        ${moduleName} ${condition}
    </a>`);
    return listItem;
};

var loadVerticesNames = function() {
    $.ajax( { 
        url: vertex_api_url+'light/',
        type: 'get',
        headers: {
            'ACTION': 'json',
        },
        success: function (data) {
            $('#available_vertices_list').empty();
            $.each(data.data, function(i, v) {
                var moduleName = v.computing_module.name
                var conditionOption = v.condition_option.label
                var conditionValue = v.condition_value.label
                $('#available_vertices_list').append(
                    makeListItem(v.id, moduleName, conditionOption, conditionValue));
            }) 
        }
    } );
};

var addOperator = function(vertexId, vertexName, conditionOption, conditionValue) {
    var operatorId = 'operator_' + vertexId;
    $.ajax( {
        url: vertex_api_url + vertexId + '/',
        type: 'get',
        headers: {
            'ACTION': 'json',
        },
        success: function(data) {
            var properties = {
                id: vertexId,
                title: vertexName,
                inputs: {},
                outputs: {},
                condition_option: conditionOption,
                condition_value: conditionValue,
            };
            if (data.data.computing_module.name == 'START') {
                properties.outputs['output_0'] = {label: 'options'};
                properties.outputs['output_1'] = {label: 'output 1'};
            } else if (data.data.computing_module.name == 'FINISH') {
                properties.inputs['input_1'] = {label: 'input 1'};
            } else {
                nInputs = data.data.computing_module.number_of_inputs;
                properties.inputs['input_0'] = {label: 'options'};
                for (i = 1; i < nInputs+1; i++) {
                    properties.inputs[`input_${i}`] = {
                        label: `input ${i}`,
                    }
                }
                nOutputs = data.data.computing_module.number_of_outputs;
                for (i = 1; i < nOutputs+1; i++) {
                    properties.outputs[`output_${i}`] = {
                        label: `output ${i}`,
                    }
                }
            }
            var operatorData = {
                top: ($flowchart.height() / 2) - 30,
                left: ($flowchart.width() / 2) - 100 + (vertexId * 10),
                properties: properties,
            }
            $flowchart.flowchart('createOperator', operatorId, operatorData);
        }
    } );
};

var addVertex = function(obj) {
    var vertexName = obj.getAttribute('module-name');
    var vertexId = obj.getAttribute('value');
    var conditionOption = obj.getAttribute('condition-option');
    var conditionValue = obj.getAttribute('condition-value');
    addOperator(vertexId, vertexName, conditionOption, conditionValue);
    $(obj).remove();
};

var sortVertices = function(listId) {
    var mylist = $(listId);
    var listitems = mylist.children('a').get();
    listitems.sort(function(a, b) {
       return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
    })
    $.each(listitems, function(idx, itm) { mylist.append(itm); });        
}

$(document).ready( function () {

    $('#id_modal_dialog').addClass('modal-dialog-wide');

    // Add new vertex button
    $(conveyor_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-vertex-form').length) {
                loadVerticesNames();
            };
            $(child_modal_id).remove();
        })
    });

    // Remove button
    $(conveyor_form_class_name).on('click', '.js-del-button', function() {
        operatorId = $flowchart.flowchart('getSelectedOperatorId');
        operatorData = $flowchart.flowchart('getOperatorData', operatorId);
        vertexId = operatorData.properties.id;
        moduleName = operatorData.properties.title;
        conditionOption = operatorData.properties.condition_option
        conditionValue = operatorData.properties.condition_value
        $('#available_vertices_list').append(
            makeListItem(vertexId, moduleName, conditionOption, conditionValue));
        $flowchart.flowchart('deleteSelected');
        sortVertices('#available_vertices_list');
    });

    // Add vertex to graph
    $(conveyor_form_class_name).on('click', '.js-add-element-button', function() {
        addVertex(this);
    });

    $flowchart.flowchart({
        onOperatorSelect: function(operatorId) {
            $('.js-del-button').attr('disabled', false);
            return true;
        },
        onOperatorUnselect: function() {
            $('.js-del-button').attr('disabled', true);
            return true;
        },
        onLinkSelect: function(linkId) {

            return true;
        },
        onLinkUnselect: function() {

            return true;
        }
    });

    loadVerticesNames();

    // Create data variable table
    datavariableOptions["ajax"] = { 'url': datavariable_api_url, 'type': 'GET', 'dataSrc': 'data' };
    var table = $('#conveyor-datavariable').DataTable( datavariableOptions );

    // Apply the plugin on a standard, empty div...
    $flowchart.flowchart({
        data: {},
        linkWidth: 3,
        distanceFromArrow: 0,
        defaultSelectedLinkColor: '#000055',
        grid: 10,
        multipleLinksOnInput: true,
        multipleLinksOnOutput: true,
        canUserEditLinks: true,
    });

} );