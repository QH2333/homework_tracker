'use strict'

document.getElementsByTagName("body")[0].onload = loadData;

Date.prototype.format = function (fmt) { // Not used (Since I have enought bandwith :) )
    var o = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S": this.getMilliseconds()
    };

    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }

    for (var k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(
                RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }

    return fmt;
}

function loadData() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4 && request.status == 200) {
            if (request.responseText == "DB Error") {
                alert("Database error!");
                return;
            }
            var response = JSON.parse(request.responseText);
            var courseid = 0;
            for (var course of response) {
                var courseHeader = createSimpleElement("div", "card-header", null);
                courseHeader.appendChild(createSimpleElement("h5", null, course.courseName));
                var courseBody = createSimpleElement("div", "card-body", null);
                var expiryFlag = false;
                var divCollapsed = createSimpleElement("div", "collapse", null);
                divCollapsed.setAttribute("id", "collapse" + courseid);
                divCollapsed.setAttribute("data-parent", "#course" + courseid);
                for (var assignment of course.assignments) {
                    var deltaTime = new Date(assignment.expiryTime) - new Date();
                    if (!expiryFlag && deltaTime < -1000 * 60 * 60 * 24)
                    {
                        expiryFlag = true;
                        var showHideBtn = createSimpleElement("h2", "mb-0 text-right", null);
                        showHideBtn.innerHTML = `
                        <button class="btn btn-secondary" id="btn-collapse${courseid}" type="button" data-toggle="collapse" data-target="#collapse${courseid}" aria-expanded="true" aria-controls="collapse${courseid}">
                            Show Previous ▼
                        </button>`
                        courseBody.appendChild(showHideBtn);
                        courseBody.appendChild(document.createElement("hr"));
                    }
                    var assignItem = createAssignment(assignment);
                    if (!expiryFlag) {
                        // Put current assignments into card-body
                        courseBody.appendChild(assignItem);
                        courseBody.appendChild(document.createElement("hr"));
                    }
                    else {
                        // Put expired assignments into div-collapsed
                        divCollapsed.appendChild(assignItem);
                        divCollapsed.appendChild(document.createElement("hr"));
                    }
                }
                // Makeup the course
                if (expiryFlag) {
                    courseBody.appendChild(divCollapsed);
                }
                var courseCard = createSimpleElement("div", "card bg-light mb-3 accordion", null);
                courseCard.setAttribute("id", "course" + (courseid++));
                courseCard.appendChild(courseHeader);
                courseCard.appendChild(courseBody);
                // Add course to the document
                document.getElementById("data").appendChild(courseCard);
            }
        }
    }
    request.open("GET", "/data", true);
    request.send();
}

function createAssignment(assignment) {
    // Assignment detail
    var assignDetail = createSimpleElement("pre", null, null);
    assignDetail.innerHTML = assignment.detail;
    // Submit: Method&Time (Assignment footer)
    var submitMethod = createSimpleElement("span", "badge badge-pill badge-primary", "Submit Method: " + assignment.method);
    var assignTime = createSimpleElement("span", "badge badge-pill badge-secondary", "Assign Time: " + assignment.assignTime);
    var assignDeadline;

    var ddlTime = new Date(assignment.expiryTime);
    var deltaTime = ddlTime - new Date();
    var ddlString = "Deadline: " + assignment.expiryTime; // Format: yyyy-MM-dd hh:mm:ss

    if (deltaTime > 1000 * 60 * 60 * 24) { // More than 24 hrs
        assignDeadline = createSimpleElement("span", "badge badge-pill badge-info", ddlString);
    } else if (deltaTime >= 0) { // Less than 24 hrs
        assignDeadline = createSimpleElement("span", "badge badge-pill badge-warning", ddlString);
    } else { // Expired
        assignDeadline = createSimpleElement("span", "badge badge-pill badge-secondary", ddlString);
    }

    var assignFooter = createSimpleElement("div", "text-right", null);
    assignFooter.appendChild(submitMethod);
    assignFooter.appendChild(createSimpleElement("span", null, " | "));
    assignFooter.appendChild(assignTime);
    assignFooter.appendChild(createSimpleElement("span", null, " "));
    assignFooter.appendChild(assignDeadline);
    // Combine detail and footer
    var assignItem = document.createElement("div");
    assignItem.appendChild(assignDetail);
    assignItem.appendChild(assignFooter);
    return assignItem;
}

function createSimpleElement(nodeType, classAttr, innerText) {
    var elem = document.createElement(nodeType);
    if (classAttr) elem.setAttribute("class", classAttr);
    if (innerText) elem.appendChild(document.createTextNode(innerText));
    return elem;
}