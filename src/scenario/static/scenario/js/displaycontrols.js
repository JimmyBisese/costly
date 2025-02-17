/*jshint esversion: 6 */
/*jshint strict:false */

/*globals $:false */

function normal(mydiv) {
    let something = mydiv.parentElement.parentElement.parentElement.querySelector('.col2');
    something.style.display = "none";
}

function hover(mydiv) {
    let something = mydiv.parentElement.parentElement.parentElement.querySelector('.col2');
    something.style.display = "block";
}


function toggleHelpText(mydivId) {
    let x = document.getElementById(mydivId);
    if (!x) {
        window.alert("toggleHelpText('" + mydivId + "') unable to find HelpText div");
    } else {
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }
}


function toggleDescription(d) {
    let description = document.getElementById(d);
    if (description.style.display !== 'block') {
        description.style.display = 'block';
    } else {
        description.style.display = 'none';
    }
}


function open_areal_features_help(button_context) {
    open_structure_help(button_context, "areal_features_header");
}


function open_nonconventional_structure_help(button_context) {
    open_structure_help(button_context, 'nonconventional');
}


function open_conventional_structure_help(button_context) {
    open_structure_help(button_context, 'conventional');
}


function open_structure_help(button_context, type) {

    let sibling_id = button_context.firstElementChild.firstElementChild.id;
    let structure_id = sibling_id.replace('checkbox_', '');

    let sourceContentDiv = document.getElementById("help_" + structure_id + "_innerHTML");

    // let help_div_id = "help_" + structure_id;
    let sourceTitleContentDiv;

    if (sourceContentDiv === null)  {
        return;
    }

    if (sourceContentDiv !== null) {
        if (sourceContentDiv.style.display === "none") {
            sourceContentDiv.style.display = "";
        } else {
            sourceContentDiv.style.display = "none";
        }
        //it's already been set up
        if (sourceContentDiv.getElementsByClassName("closebutton").length > 0) {
            return;
        }
        let sourceTitleContentDivs = sourceContentDiv.getElementsByClassName(["title"]);
        if (sourceTitleContentDivs.length === 1) {
            sourceTitleContentDiv = sourceTitleContentDivs[0];
        }

        // add a tag to the picture
        let picrightDivs = sourceContentDiv.getElementsByClassName(["picright"]);
        if (picrightDivs.length === 1) {
            let captionDiv = document.createElement("p");
            captionDiv.innerHTML = "Jenn Lenart, Tetra Tech, INC";
            captionDiv.classList.add("source");
            picrightDivs[0].appendChild(captionDiv);
        }
    }

    // let page_help_div_id = "structures_help_col";
    // let top_align_div_id = type + "_structure_header";
    // let title_tx = "TBD";

    // let pageHelpDiv = document.getElementById(page_help_div_id);
    // let topAlignDiv = document.getElementById(top_align_div_id);




    let buttonDiv = document.createElement("button");
    buttonDiv.type = "button";
    buttonDiv.classList.add("closebutton");
    buttonDiv.addEventListener("click", close_cs_help);

    let imageDiv = document.createElement("img");
    imageDiv.src = SETTINGS.URLS.IIS_PREFIX + "/static/scenario/images/close2.gif";
    imageDiv.style.border = "0";
    buttonDiv.appendChild(imageDiv);

    sourceContentDiv.classList.add("major_help");
    sourceTitleContentDiv.appendChild(buttonDiv);
    sourceTitleContentDiv.style.fontSize = "18px";
    sourceTitleContentDiv.style.fontWeight = "bold";



    sourceContentDiv.style.display = "";
}


function close_cs_help(button_context) {
    // Toggle Conventional Structure Help. Open clicked structure(, and close all others ???)
    // use the string to find the help section (which found looking for an ID which is the same string preceeded by 'cs_')
    if (button_context.parentElement === undefined) {
        //support new mouse click event
        button_context.currentTarget.parentElement.parentElement.style.display = 'none';
    } else {
        button_context.parentElement.style.display = 'none';
    }
}


function close_cost_item_help(button_context) {
    /* this is the close button on the Cost Item Unit Costs tab to close the help using the x  button */

    // let id = button_context;

    // this is confusing. there are 2 ids used  CostItemItemUnitCostsHelpText and StructureCostItemHelpText
    // this moves up the stack and finds the correct id to use to find the dom that holds the help text

    // updated - now just remove the individual help, not the whole thing
    let helpDom = document.getElementById(button_context.parentElement.parentElement.id);
    //let helpDom = document.getElementById(button_context.parentElement.id);

    //TODO: figure out how to allow multiple help things to show and only close if there are none left
    if (helpDom.style.display === 'block') {
        // now see if they are toggling off an existing help section
        let item_id = button_context.parentElement.id;

        let helpSelectedDom = helpDom.querySelector('[id="' + item_id + '"]');

        if (helpSelectedDom !== null) {
            helpSelectedDom.remove();
            if (helpDom.childElementCount === 0) {
                helpDom.style.display = 'none';
            }
        }
    }
}

function close_ci_help(button_context) {
    /* this is the close button on the Cost Item Unit Costs tab to close the help using the x  button */

    let id = button_context;

    // this is confusing. there are 2 ids used this one and StructureCostItemHelpText
    let helpDom = document.getElementById('StructureCostItemHelpText');

    //TODO: figure out how to allow multiple help things to show and only close if there are none left
    if (helpDom.style.display === 'block') {
        // now see if they are toggling off an existing help section
        let helpSelectedDom = helpDom.querySelector('[id="' + id + '"]');

        if (helpSelectedDom !== null) {
            helpDom.innerHTML = '';
            helpDom.style.display = "none";
        }
    }
}

function collapseDetail(element) {
    /* open and close the details parts.
     *  this relies on the next dom node being the thing to collapse,
     *  and the first class name being the 'name' to use */

    let className = element.nextElementSibling.classList[0];

    let elements = document.getElementsByClassName(className);

    if (elements.length > 0) {
        // let i;
        let isShowing = elements[0].classList.contains("w3-show");
        for (let i = 0; i < elements.length; i++) {
            elements[i].classList.toggle("w3-show");

            let kbButton = elements[i].previousElementSibling;
            if (kbButton !== null) {
                let classList = kbButton.className.split(" ");
                if (classList.indexOf("w3-button-open") === -1) {
                    kbButton.className += " " + "w3-button-open";
                } else {
                    kbButton.className = kbButton.className.replace(/\bw3-button-open\b/g, "");
                }
            }

        }
        /* if isShowing == true then we are closing.  collapse to 0 height */
        if (isShowing === true) {
            for (let i = 0; i < elements.length; i++) {
                elements[i].style.height = 'unset';
            }
        } else {
            let max_height = 0;
            let max_top = 0;
            for (let i = 0; i < elements.length; i++) {
                let height = elements[i].offsetHeight;
                let top = elements[i].offsetTop;
                if (height > max_height) {
                    max_height = height;
                }
                if (top > max_top) {
                    max_top = top;
                }
            }
            for (let i = 0; i < elements.length; i++) {
                elements[i].style.height = max_height;
                // get the content in the comparison column to align using top
                if (elements[i].classList.contains("comparison_column")) {
                    elements[i].style.position = 'absolute';
                    elements[i].style.top = max_top;
                }
            }
        }

    }
}

   /* open and close the details parts.
     *  this relies on the next dom node being the thing to collapse,
     *  and the first class name being the 'name' to use */
    function toggleDetail(element, boolOpen) {

        let className = element.nextElementSibling.classList[0];

        let elements = document.getElementsByClassName(className);

        if (elements.length <= 0) {
            return;
        }
        let i;
        // let isShowing = elements[0].classList.contains("w3-show");
        for (i = 0; i < elements.length; i++) {
            let classList = elements[i].className.split(" ");
            if (boolOpen === true && classList.indexOf("w3-show") === -1) {
                elements[i].className += " " + "w3-show";
            } else if (boolOpen === false && classList.indexOf("w3-show") !== -1) {
                elements[i].className = elements[i].className.replace(/\bw3-show\b/g, "");
            }
        }
        /* if isShowing == true then we are closing.  collapse to 0 height */
        if (boolOpen === true) {
            let max_height = 0;

            for (let i = 0; i < elements.length; i++) {
                let height = elements[i].offsetHeight;

                if (height > max_height) {
                    max_height = height;
                }
            }
            for (let i = 0; i < elements.length; i++) {
                elements[i].style.height = max_height;
            }
        } else {
            for (let i = 0; i < elements.length; i++) {
                elements[i].style.height = 'unset';
            }
        }
    }

    function expandAllDetail(element) {
        let resultDetails = document.getElementsByClassName('resultDetails');
        for (let j = 0; j < resultDetails.length; j++) {
            let kbButtons = resultDetails[j].getElementsByClassName("w3-container-button");
            for (let i = 0; i < kbButtons.length; i++) {
                let classList = kbButtons[i].className.split(" ");
                if (classList.indexOf("w3-button-open") === -1) {
                    kbButtons[i].className += " " + "w3-button-open";
                }
                toggleDetail(kbButtons[i], true);
            }
        }
        // let button_text = 'Areal Features';
        let top_of_areal_features = $('button:contains("Land Cover")').offset().top;
        let areal_features_dom = document.getElementsByClassName('areal_features');
        // areal_features_dom[2].clientTop = top_of_areal_features;
        resultDetails[2].style.top = top_of_areal_features;
    }


    function collapseAllDetail(element) {
        let resultDetails = document.getElementsByClassName('resultDetails');
        for (let j = 0; j < resultDetails.length; j++) {
            let kbButtons = resultDetails[j].getElementsByClassName("w3-container-button");
            for (let i = 0; i < kbButtons.length; i++) {
                let classList = kbButtons[i].className.split(" ");
                if (classList.indexOf("w3-button-open") !== -1) {
                    kbButtons[i].className = kbButtons[i].className.replace(/\bw3-button-open\b/g, "");
                }
                toggleDetail(kbButtons[i], false);
            }
        }
    }




//
// function toggle_structure_help(cs_option, button_context) {
//
//     if (button_context !== null)
//     {
//         // get the id of the input that this label is connected too. i.e. ui_stormwater_wetland
//         sibling_id = button_context.nextElementSibling.id;
//
//         if (button_context.classList.contains("closebutton"))
//         {
//             button_context.parentElement.style.display = 'none';
//             return;
//         }
//     }
//
//     let structure_id = 'cs_' + cs_option;
//     let help_section = document.getElementById(structure_id);
//
//     if (! help_section){
//         window.alert("There is no help section found for cs_option: '" + cs_option + "'");
//     }
//     else {
//         help_section.style.display = (help_section.style.display === 'block') ? 'none' : 'block';
//
//         for (let i in arr_conventional_structures) {
//
//             if (cs_option !== arr_conventional_structures[i]) {
//                 let structure_id = 'cs_' + arr_conventional_structures[i];
//                 let help_section = document.getElementById(structure_id);
//
//                 if (help_section) {
//                     help_section.style.display = "none";
//                 }
//
//                 //TODO would it be best to display the help stuff at the page height level as the link used to access it?
//                 //document.getElementById('inputs').scrollTop = 0;
//             }
//         }
//     }
// }

