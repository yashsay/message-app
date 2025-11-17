import PropTypes from "prop-types";
import "./Header.scss";

const Header = ({ title = "IntelliChat" }) => (
  <header className="header">
    <div className="header__logo">
      <h1 className="header__title">{title}</h1>
    </div>
  </header>
);

Header.propTypes = {
  title: PropTypes.string,
};

export default Header;
