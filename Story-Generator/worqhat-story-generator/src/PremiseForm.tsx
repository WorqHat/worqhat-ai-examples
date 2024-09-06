import React, { useState } from "react";

interface PremiseFormProps {
  onSubmit: (premise: string) => void;
}

const PremiseForm: React.FC<PremiseFormProps> = ({ onSubmit }) => {
  const [premiseInput, setPremiseInput] = useState<string>("");

  const randomPremises: string[] = [
    "A young boy discovers he has magical powers",
    "A detective who solves crimes using telepathy",
    "An astronaut stranded on Mars with only a robot for company",
  ];

  const handleRandomPremise = () => {
    const randomPremise =
      randomPremises[Math.floor(Math.random() * randomPremises.length)];
    onSubmit(randomPremise);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(premiseInput);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter a premise"
          value={premiseInput}
          onChange={(e) => setPremiseInput(e.target.value)}
        />
        <button type="submit">Submit Premise</button>
      </form>
      <button onClick={handleRandomPremise}>Surprise Me!</button>
    </div>
  );
};

export default PremiseForm;
