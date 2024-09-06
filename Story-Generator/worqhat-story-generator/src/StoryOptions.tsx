import React from "react";

interface StoryOptionsProps {
  options: string[];
  onSelect: (option: string) => void;
}

const StoryOptions: React.FC<StoryOptionsProps> = ({ options, onSelect }) => {
  const handleSelection = (option: string) => {
    onSelect(option);
  };

  return (
    <div>
      <h2>Select a Story Option:</h2>
      {options.map((option, index) => (
        <div key={index}>
          <input
            type="radio"
            name="story-option"
            id={`option-${index}`}
            value={option}
            onChange={() => handleSelection(option)}
          />
          <label htmlFor={`option-${index}`}>{option}</label>
        </div>
      ))}
    </div>
  );
};

export default StoryOptions;
