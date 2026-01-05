let students = [
  {name: 'Alice', grade: 85, subject: 'Math', credits: 3},
  {name: 'Bob', grade: 92, subject: 'English', credits: 4},
  {name: 'Alice', grade: 78, subject: 'Science', credits: 4},
  {name: 'Charlie', grade: 88, subject: 'Math', credits: 3},
  {name: 'Bob', grade: 95, subject: 'Math', credits: 3},
  {name: 'Charlie', grade: 72, subject: 'English', credits: 4},
  {name: 'Alice', grade: 90, subject: 'English', credits: 4},
  {name: 'Charlie', grade: 85, subject: 'Science', credits: 4}
];

function getStudentAverages(students) {
    let nameCount = {}
    let sumD = students.reduce((a, n) => {
        if(!a[n.name]){
            a[n.name] = 0
            nameCount[n.name] = 0
        }
        a[n.name] += n.grade
        nameCount[n.name] += 1
        return a
    }, {})
    Object.keys(sumD).forEach(key => {
        sumD[key] /= nameCount[key]
    });
    return sumD
}

function getTopStudentPerSubject(students) {
  return students.reduce((a, n) => {
    if(!a[n.subject]){
        a[n.subject] = {name: n.name, grade: n.grade}
    }
    if(a[n.subject]["grade"] < n.grade){
       a[n.subject]["name"] = n.name 
       a[n.subject]["grade"] = n.grade 
    }
    return a
  }, {})
}

function getWeightedGPA(students) {
  let countCredit = {};
  let total = students.reduce((a,n) => {
    if(!a[n.name]){
        a[n.name] = 0
        countCredit[n.name] = 0;
    }
    a[n.name] += n.grade * n.credits;
    countCredit[n.name] += n.credits;
    return a;
  }, {})
  Object.keys(total).forEach(key => {
    total[key] /= countCredit[key]
  });
  return total;
}

function getStudentsAboveThreshold(students, threshold) {
  // Your code here
  // Return array of unique student names
  let qualify = students.filter(n => n.grade >= threshold) // This remove all student with bellow threshold
  let list = qualify.map(n => n = n.name) // This transform element form the whole info of a student to just name

  return [...new Set(list)]; // this remove duplicate
}

function getComprehensiveReport(students) {
  // Your code here
  // Return object with:
  // - totalStudents: number of unique students
  // - totalClasses: total number of class records
  // - averageGrade: average of ALL grades
  // - subjectStats: object with each subject's average grade
  // - topPerformer: student with highest weighted GPA
  let totalGrade = students.reduce((a,n) => {
    a += n.grade
    return a
  },0)
  let avg = totalGrade / students.length

  let subCount = {}
  let eachSub = students.reduce((a, n) => {
    if(!a[n.subject]){
        a[n.subject] = 0
        subCount[n.subject] = 0
    }
    a[n.subject] += n.grade
    subCount[n.subject] += 1
    return a
  }, {})
  Object.keys(eachSub).forEach(key => {
    eachSub[key] /= subCount[key]
  })

  let allGPA = getWeightedGPA(students);
  let bestGPA = { name: '', gpa: 0 }
  Object.keys(allGPA).forEach(key => {
    if(bestGPA.gpa < allGPA[key]){
        bestGPA.gpa = allGPA[key]
        bestGPA.name = key
    }
  })

  let summary = {
    totalStudents: Object.keys(getStudentAverages(students)).length,
    totalClasses: students.length,
    averageGrade: avg,
    subjectStats: eachSub,
    topPerformer: bestGPA
  }

  return summary
}

console.log(getComprehensiveReport(students));
// console.log(getStudentsAboveThreshold(students, 90));
// console.log(getWeightedGPA(students));
// console.log(getTopStudentPerSubject(students));
// console.log(getStudentAverages(students));
