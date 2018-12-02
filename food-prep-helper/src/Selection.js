import React, { Component } from 'react';

const SelectionHeader = () => {
    return (
        <thead>
            <tr>
                <th>Day</th>
                <th>Breakfast</th>
                <th>Lunch</th>
                <th>Dinner</th>
            </tr>
        </thead>
    );
}

// for each day,meal pair, there should be one recipe selection. Push that
// to recipesPicked array onChange, or handle by onSubmit. If not, would need
// to be able to change recipe for day, meal in array
class SelectionBody extends Component {
    constructor(props) {
        super(props);
        this.initialState = {
            recipesPicked: []
        };

        this.state = this.initialState;
    }

    handleChange = event => {
        const { recipe, value } = event.target;

        console.log("handle change");

        this.setState({
            [recipe] : value
        });
    }

    render () {
        // TODO add options to list recipes with same meal from Python scripts
        // TODO add key:value (day+meal:recipe) to state variable and pass to
        // GroceryList component
        const { daysToPlanFor } = this.props;
        const meals = ["Breakfast", "Lunch", "Dinner"];

        const selectionRows = daysToPlanFor.map((day, index) => {
            return (
                <tr key={index}>
                    <td>{day}</td>
                    <td>
                        <select>
                            <option value="none"></option>
                            <option
                                key={day}
                                value="recipe">
                                Recipe for meal
                            </option>
                        </select>
                    </td>
                    <td>
                        <select>
                            <option value="none"></option>
                            <option
                                key={day}
                                value="recipe">
                                Recipe for meal
                            </option>
                        </select>
                    </td>
                    <td>
                        <select>
                            <option value="none"></option>
                            <option
                                key={day}
                                value="recipe">
                                Recipe for meal
                            </option>
                        </select>
                    </td>
                </tr>
            );
        });

        return (
            <tbody onChange={this.handleChange}>{selectionRows}</tbody>
        );
    }
}

class Selection extends Component {
    render () {
        const { daysToPlanFor } = this.props;

        return (
            <table>
                <SelectionHeader />
                <SelectionBody daysToPlanFor={daysToPlanFor} />
            </table>
        );
    }
}

export default Selection;
