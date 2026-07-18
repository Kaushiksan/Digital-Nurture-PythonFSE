function Header(props) {

    return (

        <header className="header">

            <h1>
                {props.siteName}
            </h1>


            <nav>

                <a href="#home">
                    Home
                </a>

                <a href="#courses">
                    Courses
                </a>

                <a href="#profile">
                    Profile
                </a>

            </nav>


            <div className="enrolled-count">

                Enrolled Courses: {
                    props.enrolledCount
                }

            </div>

        </header>

    );

}


export default Header;
