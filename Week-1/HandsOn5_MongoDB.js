// ==========================================================
// HANDS-ON 5
// MongoDB - Document Modelling, CRUD & Aggregation
// ==========================================================

// ==========================================================
// TASK 1 : Create Database & Collection
// ==========================================================

// Create / Switch Database

use("college_nosql");

// Create Collection

db.createCollection("feedback");

// ==========================================================
// Insert Sample Documents
// ==========================================================

db.feedback.insertMany([

{
    student_id:1,
    course_code:"CS101",
    semester:"2022-ODD",
    rating:5,
    comments:"Excellent teaching. Would recommend.",
    tags:["challenging","well-structured","good-examples"],
    submitted_at:new Date("2022-11-30T10:15:00Z"),
    attachments:[
        {
            filename:"notes.pdf",
            size_kb:240
        }
    ]
},

{
    student_id:2,
    course_code:"CS101",
    semester:"2022-ODD",
    rating:4,
    comments:"Interesting subject.",
    tags:["challenging","practical"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"assignment.pdf",
            size_kb:180
        }
    ]
},

{
    student_id:3,
    course_code:"CS101",
    semester:"2022-EVEN",
    rating:5,
    comments:"Very informative.",
    tags:["good-examples","challenging"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"lab.pdf",
            size_kb:320
        }
    ]
},

{
    student_id:4,
    course_code:"CS102",
    semester:"2022-ODD",
    rating:4,
    comments:"Database concepts were clear.",
    tags:["sql","well-structured"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"db.pdf",
            size_kb:210
        }
    ]
},

{
    student_id:5,
    course_code:"CS102",
    semester:"2022-EVEN",
    rating:2,
    comments:"Need more practical sessions.",
    tags:["slow","review"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"feedback.pdf",
            size_kb:140
        }
    ]
},

{
    student_id:6,
    course_code:"CS103",
    semester:"2022-ODD",
    rating:3,
    comments:"Average experience.",
    tags:["oops","coding"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"oops.pdf",
            size_kb:160
        }
    ]
},

{
    student_id:7,
    course_code:"EC101",
    semester:"2021-EVEN",
    rating:1,
    comments:"Very difficult.",
    tags:["tough","challenging"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"ec.pdf",
            size_kb:260
        }
    ]
},

{
    student_id:8,
    course_code:"ME101",
    semester:"2022-ODD",
    rating:5,
    comments:"Excellent faculty.",
    tags:["mechanical","excellent"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"me.pdf",
            size_kb:120
        }
    ]
},

{
    student_id:9,
    course_code:"CS103",
    semester:"2022-ODD",
    rating:2,
    comments:"Assignments were difficult.",
    tags:["coding","review"],
    submitted_at:new Date(),
    attachments:[
        {
            filename:"assignment2.pdf",
            size_kb:175
        }
    ]
},

// Document WITHOUT attachments
// Required by handbook

{
    student_id:10,
    course_code:"CS101",
    semester:"2022-ODD",
    rating:5,
    comments:"Loved the examples.",
    tags:["good-examples","challenging"],
    submitted_at:new Date()
}

]);

// ==========================================================
// Verification
// ==========================================================
  

db.feedback.countDocuments();

db.feedback.find().pretty();

// ==========================================================
// TASK 2 : CRUD OPERATIONS
// ==========================================================

// ----------------------------------------------------------
// READ OPERATIONS
// ----------------------------------------------------------

// 1. Find all feedback with rating >= 4

db.feedback.find(
    { rating: { $gte: 4 } }
).pretty();

// ----------------------------------------------------------

// 2. Find all CS101 feedback

db.feedback.find(
    { course_code: "CS101" }
).pretty();

// ----------------------------------------------------------

// 3. Find documents containing tag "challenging"

db.feedback.find(
    { tags: "challenging" }
).pretty();

// ----------------------------------------------------------

// 4. Find feedback without attachments

db.feedback.find(
    { attachments: { $exists: false } }
).pretty();

// ----------------------------------------------------------

// 5. Find comments containing "Excellent"

db.feedback.find(
    { comments: /Excellent/i }
).pretty();

// ==========================================================
// UPDATE OPERATIONS
// ==========================================================

// Increase rating of Student 5

db.feedback.updateOne(
{
    student_id:5
},
{
    $set:{
        rating:3
    }
}
);

// ----------------------------------------------------------

// Add tag "recommended" to Student 1

db.feedback.updateOne(
{
    student_id:1
},
{
    $addToSet:{
        tags:"recommended"
    }
}
);

// ----------------------------------------------------------

// Add attachment to Student 10

db.feedback.updateOne(
{
    student_id:10
},
{
    $set:{
        attachments:[
        {
            filename:"feedback.pdf",
            size_kb:180
        }]
    }
}
);

// ==========================================================
// DELETE OPERATIONS
// ==========================================================

// Delete feedback with rating = 1

db.feedback.deleteOne(
{
    rating:1
}
);

// ----------------------------------------------------------

// Delete all reviews having rating less than 2

db.feedback.deleteMany(
{
    rating:{
        $lt:2
    }
}
);

// ==========================================================
// VERIFY CRUD
// ==========================================================

db.feedback.find().pretty();

db.feedback.countDocuments();

// ==========================================================
// ADDITIONAL QUERY PRACTICE
// ==========================================================

// Sort by rating descending

db.feedback.find()
.sort({rating:-1})
.pretty();

// ----------------------------------------------------------

// Latest feedback first

db.feedback.find()
.sort({submitted_at:-1})
.pretty();

// ----------------------------------------------------------

// Show only student_id and rating

db.feedback.find(
{},
{
    _id:0,
    student_id:1,
    rating:1
}
);

// ----------------------------------------------------------

// Count feedback for CS101

db.feedback.countDocuments(
{
    course_code:"CS101"
});

// ----------------------------------------------------------

// Average rating using aggregation preview

db.feedback.aggregate([
{
    $group:{
        _id:null,
        averageRating:{
            $avg:"$rating"
        }
    }
]);

// ==========================================================
// TASK 3 : AGGREGATION PIPELINES
// ==========================================================

// ----------------------------------------------------------
// 1. Average Rating for each Course
// ----------------------------------------------------------

db.feedback.aggregate([
{
    $group:{
        _id:"$course_code",
        Average_Rating:{$avg:"$rating"},
        Total_Feedback:{$sum:1}
    }
},
{
    $sort:{Average_Rating:-1}
}
]);

// ----------------------------------------------------------
// 2. Number of Feedback per Semester
// ----------------------------------------------------------

db.feedback.aggregate([
{
    $group:{
        _id:"$semester",
        Total_Feedback:{$sum:1}
    }
},
{
    $sort:{_id:1}
}
]);

// ----------------------------------------------------------
// 3. Average Rating above 3
// ----------------------------------------------------------

db.feedback.aggregate([
{
    $group:{
        _id:"$course_code",
        Average_Rating:{$avg:"$rating"}
    }
},
{
    $match:{
        Average_Rating:{$gt:3}
    }
}
]);

// ----------------------------------------------------------
// 4. Most Frequently Used Tags
// ----------------------------------------------------------

db.feedback.aggregate([
{
    $unwind:"$tags"
},
{
    $group:{
        _id:"$tags",
        Count:{$sum:1}
    }
},
{
    $sort:{Count:-1}
}
]);

// ----------------------------------------------------------
// 5. Top 3 Highest Rated Feedback
// ----------------------------------------------------------

db.feedback.aggregate([
{
    $sort:{rating:-1}
},
{
    $limit:3
},
{
    $project:{
        _id:0,
        student_id:1,
        course_code:1,
        rating:1,
        comments:1
    }
}
]);

// ==========================================================
// TASK 4 : CREATE INDEX
// ==========================================================

// Create Compound Index

db.feedback.createIndex({
    course_code:1,
    submitted_at:-1
});

// Verify Indexes

db.feedback.getIndexes();

// ==========================================================
// TASK 5 : EXPLAIN PLAN
// ==========================================================

db.feedback.find({
    course_code:"CS101"
}).explain("executionStats");

// ==========================================================
// VERIFICATION
// ==========================================================

print("\n========== TOTAL DOCUMENTS ==========");

print(db.feedback.countDocuments());

print("\n========== SAMPLE DOCUMENT ==========");

db.feedback.findOne();

print("\n========== INDEXES ==========");

db.feedback.getIndexes();

// ==========================================================
// COMMENTS
// ==========================================================

/*

Hands-On 5
MongoDB CRUD & Aggregation

Topics Covered

1. Create Database
2. Create Collection
3. Insert Documents
4. Read Operations
5. Update Operations
6. Delete Operations
7. Aggregation Pipeline
8. $match
9. $group
10. $project
11. $sort
12. $limit
13. $unwind
14. Compound Index
15. explain()

Expected Outcome

✔ Database Created
✔ Collection Created
✔ 10+ Documents Inserted
✔ CRUD Operations Performed
✔ Aggregation Pipelines Executed
✔ Compound Index Created
✔ Query Plan Verified

Status : COMPLETED

*/

// ==========================================================
// END OF HANDS-ON 5
// ==========================================================
