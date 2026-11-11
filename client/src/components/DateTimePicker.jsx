import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function DateTimePicker({ value, onChange }) {
  return (
    <DatePicker
      selected={value}
      onChange={onChange}
      showTimeSelect
      timeIntervals={30}
      dateFormat="MMMM d, yyyy h:mm aa"
      className="w-full p-3
        border rounded-md
        bg-gray-50
        hover:bg-gray-100
        cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500"
      calendarClassName="rounded-lg border shadow-lg"
    />
  );
}

export default DateTimePicker;