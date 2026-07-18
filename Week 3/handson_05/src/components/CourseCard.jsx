function CourseCard({
    id,
    name,
    code,
    credits,
    grade,
    onEnroll
}) {

    return (

        <article className="course-card">

            <h3>
                {name}
            </h3>


            <p>

                Course Code:

                <strong>
                    {" "}{code}
                </strong>

            </p>


            <p>

                Credits:

                <strong>
                    {" "}{credits}
                </strong>

            </p>


            <p>

                Grade:

                <strong>
                    {" "}{grade}
                </strong>

            </p>


            <button
                type="button"
                onClick={() => onEnroll(id)}
            >

                Enroll

            </button>

        </article>

    );

}


export default CourseCard;
