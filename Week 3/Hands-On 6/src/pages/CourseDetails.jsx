import { useParams } from "react-router-dom";

import { useContext } from "react";

import { CourseContext } from "../context/CourseContext";

function CourseDetails() {

    const { id } = useParams();

    const { courseList } = useContext(CourseContext);

    const course = courseList.find(

        c => c.id === Number(id)

    );

    if (!course) {

        return <h2>Course Not Found</h2>;

    }

    return (

        <section className="page">

            <h2>{course.name}</h2>

            <p>Course Code : {course.code}</p>

            <p>Credits : {course.credits}</p>

            <p>Instructor : {course.instructor}</p>

        </section>

    );

}

export default CourseDetails;
