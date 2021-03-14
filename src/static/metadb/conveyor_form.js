var conveyor_form_class_name = '.js-conveyor-form';
var vertex_api_url = $(conveyor_form_class_name).attr('vertices-url')
var datavariable_api_url = $(conveyor_form_class_name).attr('datavariables-url')
    
// Create graph container
var $flowchart = $('#conveyor_editor');
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

var makeVertexItem = function(id, moduleName, conditionOption, conditionValue) {
    var classes = "list-group-item js-add-vertex";
    var condition = '';
    if (conditionValue != '-') {
        condition = `[if ${conditionOption} == ${conditionValue}]`
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

var loadVerticesNames = function(refreshList=false) {
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
                    makeVertexItem(v.id, moduleName, conditionOption, conditionValue));
            });
            if (!refreshList) {
                loadGraph($(conveyor_form_class_name).attr('action'), $flowchart);
            }
        }
    } );
};

var makeDataVariableItem = function(id, label) {
    var classes = "list-group-item js-add-datavariable disabled";
    var listItem = $(`<a href="#" class="${classes}" value="${id}">${label}</a>`);
    return listItem;
}

var loadDataVariablesNames = function() {
    $.ajax( { 
        url: datavariable_api_url,
        type: 'get',
        headers: {
            'ACTION': 'json',
        },
        success: function (data) {
            $('#available_datavariables_list').empty();
            $.each(data.data, function(i, v) {
                $('#available_datavariables_list').append(
                    makeDataVariableItem(v.id, v.label));
            });
        }
    } );
    
};

var addOperator = function(vertexId, moduleName, conditionOption, conditionValue) {
    var operatorId = 'operator_' + vertexId;
    $.ajax( {
        url: vertex_api_url + vertexId + '/',
        type: 'get',
        headers: {
            'ACTION': 'json',
        },
        success: function(data) {
            var properties = {
                title: moduleName,
                inputs: {},
                outputs: {},
                condition_option: conditionOption,
                condition_value: conditionValue,
                autoInputs: false,
                autoOutputs: false,
            };
            var nInputs = data.data.computing_module.number_of_inputs;
            var nOutputs = data.data.computing_module.number_of_outputs;
            if (nInputs == null) {
                properties.inputs['input_1'] = {label: 'input 1'};
                properties.autoInputs = true;
            } else {
                if (nInputs > 0 && nOutputs > 0) {
                    properties.inputs['input_0'] = {label: 'options'};
                }
                for (i = 1; i < nInputs+1; i++) {
                    properties.inputs[`input_${i}`] = {
                        label: `input ${i}`,
                    }
                }
            }
            if (nOutputs == null) {
                properties.outputs['output_0'] = {label: 'options'};
                properties.outputs['output_1'] = {label: 'output 1'};
                properties.autoOutputs = true;
            } else {
                for (i = 1; i < nOutputs+1; i++) {
                    properties.outputs[`output_${i}`] = {
                        label: `output ${i}`,
                    }
                }
            }
            var operatorData = {
                top: ($flowchart.height() / 2) - 30,
                left: ($flowchart.width() / 2) - 100 + (vertexId * 10),
                vertex_id: vertexId,
                properties: properties,
            }
            $flowchart.flowchart('createOperator', operatorId, operatorData);
        }
    } );
};

var addVertex = function(obj) {
    var moduleName = obj.getAttribute('module-name');
    var vertexId = obj.getAttribute('value');
    var conditionOption = obj.getAttribute('condition-option');
    var conditionValue = obj.getAttribute('condition-value');
    addOperator(vertexId, moduleName, conditionOption, conditionValue);
    //$(obj).remove();
};

var assignDataVariable = function(obj) {
    var linkId = $flowchart.flowchart('getSelectedLinkId');
    var linkData = $flowchart.flowchart('getLinkData', linkId);
    linkData['label'] = obj.text;
    linkData['datavariable_id'] = obj.getAttribute('value');
    $flowchart.flowchart('setLinkData', linkId, linkData);
}

var sortList = function(listId) {
    var mylist = $(listId);
    var listitems = mylist.children('a').get();
    listitems.sort(function(a, b) {
       return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
    })
    $.each(listitems, function(idx, itm) { mylist.append(itm); });        
}

saveConveyor = function(e) {
    e.stopImmediatePropagation();
    var form = $(this);
    var modal_id = '#'+getModalName('parent');
    var data = $flowchart.flowchart('getData');
    data['conveyorLabel'] = $('#id_label').val();
    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: {'data': JSON.stringify(data)},
        dataType: 'json',
        success: function(response) {
            if (response.form_is_valid) {
                $.fn.dataTable.tables( {visible: false, api: true} ).ajax.reload();
                $(modal_id).modal('hide');
            }
            else {
                $.each(response.errors, function(i, v) {
                    alert(v);
                })
                $flowchart.flowchart('setData', response.data);
            }
        },
        error: function(xhr, errmsg, err) {
            console.error('Error occured when saving conveyor data');
        },
    });
    return false;
};

$(document).ready( function () {

    $('#id_modal_dialog').addClass('modal-dialog-wide');

    // Add new vertex button
    $(conveyor_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-vertex-form').length) {
                loadVerticesNames(true);
            };
            if ($('.js-datavariable-form').length) {
                loadDataVariablesNames();
            };
            $(child_modal_id).remove();
        })
    });

    // Remove vertex button
    $(conveyor_form_class_name).on('click', '.js-del-vertex-button', function() {
        operatorId = $flowchart.flowchart('getSelectedOperatorId');
        operatorData = $flowchart.flowchart('getOperatorData', operatorId);
        vertexId = operatorData.vertex_id;
        moduleName = operatorData.properties.title;
        conditionOption = operatorData.properties.condition_option
        conditionValue = operatorData.properties.condition_value
        $('#available_vertices_list').append(
            makeVertexItem(vertexId, moduleName, conditionOption, conditionValue));
        $flowchart.flowchart('deleteSelected');
        sortList('#available_vertices_list');
    });

    // Remove link button
    $(conveyor_form_class_name).on('click', '.js-del-link-button', function() {
        $flowchart.flowchart('deleteSelected');
    });

    // Add vertex to graph
    $(conveyor_form_class_name).on('click', '.js-add-vertex', function() {
        addVertex(this);
    });

    // Assign data variable to link
    $(conveyor_form_class_name).on('click', '.js-add-datavariable', function() {
        assignDataVariable(this);
    });

    // New Submit event handler
    $(conveyor_form_class_name).off('submit');
    $(conveyor_form_class_name).on('submit', function(e) {
        saveConveyor.call(this, e);
        return false; 
    });

    $flowchart.flowchart({
        onOperatorSelect: function(operatorId) {
            $('.js-del-vertex-button').attr('disabled', false);
            return true;
        },
        onOperatorUnselect: function() {
            $('.js-del-vertex-button').attr('disabled', true);
            return true;
        },
        onOperatorCreate: function(operatorId, operatorData, fullElement) {
            $(`.js-add-vertex[value="${operatorData.vertex_id}"]`).remove();
            return true
        },
        onLinkSelect: function(linkId) {
            $('.js-del-link-button').attr('disabled', false);
            $('#available_datavariables_list *').each( function(i, v) {
                $(v).removeClass('disabled');
            });
            return true;
        },
        onLinkUnselect: function() {
            $('.js-del-link-button').attr('disabled', true);
            $('#available_datavariables_list *').each( function(i, v) {
                $(v).addClass('disabled');
            });
            return true;
        },
        onLinkCreate: function(linkId, linkData) {
            var operatorData = $flowchart.flowchart('getOperatorData', linkData.fromOperator);
            if (operatorData.properties.autoOutputs) {
                pos = parseInt(linkData.fromConnector.split('_')[1], 10) + 1;
                operatorData.properties.outputs[`output_${pos}`] = {label: `output ${pos}`};
                $flowchart.flowchart('setOperatorData', linkData.fromOperator, operatorData);
            };

            var operatorData = $flowchart.flowchart('getOperatorData', linkData.toOperator);
            if (operatorData.properties.autoInputs) {
                pos = parseInt(linkData.toConnector.split('_')[1], 10) + 1;
                operatorData.properties.inputs[`input_${pos}`] = {label: `input ${pos}`};
                $flowchart.flowchart('setOperatorData', linkData.toOperator, operatorData);
            };
            return true;
        },
    });

    loadVerticesNames(false);
    loadDataVariablesNames();
} );