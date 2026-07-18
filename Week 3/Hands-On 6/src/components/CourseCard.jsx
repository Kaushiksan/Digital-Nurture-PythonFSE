import { Link } from "react-router-dom";

function CourseCard({ course }) {

    return (

        <div className="course-card">

            <h3>{course.name}</h3>

            <p>Code : {course.code}</p>

            <p>Credits : {course.credits}</p>

            <Link to={`/courses/${course.id}`}>

                View Details

            </Link>

        </div>

    );

}

export default CourseCard;
