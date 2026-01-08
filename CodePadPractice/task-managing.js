let tasks = [
  {id: 1, title: 'Fix LOGIN bug', assignee: 'Alice', priority: 'HIGH', status: 'done', hours: 5, tags: ['bug', 'urgent']},
  {id: 2, title: 'Add user dashboard', assignee: 'Bob', priority: 'MEDIUM', status: 'in-progress', hours: 12, tags: ['feature']},
  {id: 3, title: 'Update API docs', assignee: 'Alice', priority: 'LOW', status: 'done', hours: 3, tags: ['docs']},
  {id: 4, title: 'Refactor AUTH module', assignee: null, priority: 'HIGH', status: 'todo', hours: 8, tags: ['refactor', 'urgent']},
  {id: 5, title: 'Fix PAYMENT gateway', assignee: 'Charlie', priority: 'CRITICAL', status: 'in-progress', hours: 15, tags: ['bug', 'urgent']},
  {id: 6, title: 'Design new homepage', assignee: 'Bob', priority: 'MEDIUM', status: 'done', hours: 10, tags: ['design', 'feature']},
  {id: 7, title: 'Optimize DATABASE queries', assignee: 'Alice', priority: 'HIGH', status: 'todo', hours: 6, tags: ['performance']},
  {id: 8, title: '', assignee: 'Invalid', priority: 'LOW', status: 'done', hours: 0, tags: []},  // Edge case: empty title
  {id: 9, title: 'Setup CI/CD pipeline', assignee: 'Charlie', priority: 'MEDIUM', status: 'in-progress', hours: null, tags: ['devops']}  // Edge case: null hours
];

const mapping = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}

function getValidTasks(tasks) {
  return tasks.filter(n => n.title !== "" && n.assignee !== null && n.hours > 0 && n.tags.length >= 1)
}

// Another way
// tasks.filter(n => {
//   return n.title !== "" && 
//          n.assignee !== null && 
//          n.hours > 0 && 
//          n.tags.length >= 1;
// })

function extractKeywords(tasks) {
  // Find all UPPERCASE words in titles
  // Return {keyword: count}
  return tasks.reduce((a, n) => {
    let sep = n.title.split(' ')
    for(let i = 0; i < sep.length; i++){
        // The 2nd check: word !== word.toLowerCase()  // "123" !== "123" → false ✗ FAILS HERE! 
        // PREVENT NUMBER?????
        if(sep[i] === sep[i].toUpperCase() && sep[i] !== sep[i].toLowerCase() && sep[i].length > 0){
            if(!a[sep[i]]){
                a[sep[i]] = 0;
            }
                a[sep[i]] += 1;
        }
    }
    return a
  }, {})
}


function getAssigneeWorkload(tasks) {
  // Return {assignee: totalPriorityScore}
  return tasks.reduce((a,n) => {
    if(!a[n.assignee] && n.status === 'in-progress'){
        a[n.assignee] = 0
    }
    if(n.status === 'in-progress'){
        a[n.assignee] += mapping[n.priority]
    }
    return a
  }, {})
}

function getTagAnalytics(tasks) {
  // Return {tag: {count, totalHours, avgPriority}}
  let temp = tasks.reduce((a,n) => {
    let tagArr = n.tags
    for(let i = 0; i < tagArr.length; i++){
        if(!a[tagArr[i]]){
            a[tagArr[i]] = {count: 0, totalHours: 0, avgPriority: 0}
        }
        a[tagArr[i]].count += 1
        a[tagArr[i]].totalHours += (n.hours || 0) // Treat null as 0
        a[tagArr[i]].avgPriority += mapping[n.priority]
    }
    return a
  }, {})
  Object.keys(temp).forEach(keys => {
    temp[keys].avgPriority /= temp[keys].count
  })
  return temp
}

function getDoneTaskThatIsValid(tasks){
  let validTasks = getValidTasks(tasks)
  return validTasks.filter(n => n.status === 'done')
}

function getProjectDashboard(tasks) {
  let validTasksNum = getValidTasks(tasks).length
  let totalValidHours = getValidTasks(tasks).reduce((a,n) => a + n.hours, 0)
  let allKeyWord = extractKeywords(tasks)
  let mostCommonKW 
  let mostCommonKWCount = 0 
  let assigneeScores = getAssigneeWorkload(tasks)
  let assigneeRanks = []
  Object.keys(assigneeScores).forEach(key => {
    assigneeRanks.push([key, assigneeScores[key]])
  })
  assigneeRanks = assigneeRanks.sort((a,b) => b[1] - a[1])
  Object.keys(allKeyWord).forEach(key => {
    if(mostCommonKWCount < allKeyWord[key]){
      mostCommonKW = key
      mostCommonKWCount = allKeyWord[key]
    }
  })
  let bt
  let btCount = 0
  let bestTags = tasks.reduce((a,n) => {
    let tagArr = n.tags
    for(let i = 0; i < tagArr.length; i++){
        if(!a[tagArr[i]]){
            a[tagArr[i]] = 0
        }
        a[tagArr[i]] += 1
    }
    return a
  }, {})
  Object.keys(bestTags).forEach(key => {
    if(btCount < bestTags[key]){
      bt = key
      btCount = bestTags[key]
    }
  })
  let critAndProgress = tasks.filter(n => n.status === 'in-progress' && n.priority === 'CRITICAL').map(t => t.title)
  let unassignCritHigh = tasks.filter(n => n.assignee === null && (n.priority === 'CRITICAL' || n.priority === 'HIGH'))
  return {
    validTaskCount: validTasksNum,
    invalidTaskCount: tasks.length - validTasksNum,
    completionRate: (getDoneTaskThatIsValid(tasks).length/validTasksNum) * 100,
    totalHours: totalValidHours,
    topKeyword: mostCommonKW,
    criticalInProgress: critAndProgress,
    assigneeRankings: assigneeRanks,
    mostUsedTag: bt,
    unassignedHighPriority: unassignCritHigh.length
  };
}

// Example for 'bug' tag:
// Tasks 1 and 5 have 'bug'
// count: 2
// totalHours: 5 + 15 = 20
// avgPriority: (3 + 4) / 2 = 3.5

// console.log(getAssigneeWorkload(tasks));
// Expected: { Bob: 2, Charlie: 4 }
// Bob has task 2 (MEDIUM, in-progress) = 2
// Charlie has task 5 (CRITICAL, in-progress) = 4
// console.log(extractKeywords(tasks));
// Expected: { LOGIN: 1, API: 1, AUTH: 1, PAYMENT: 1, DATABASE: 1, CI: 1, CD: 1 }
// console.log(getValidTasks(tasks).length);  // Should be 6 (removes ids 4, 8, 9)
