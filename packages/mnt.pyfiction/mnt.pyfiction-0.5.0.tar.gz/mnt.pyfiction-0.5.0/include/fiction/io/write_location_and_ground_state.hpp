//
// Created by Jan Drewniok on 09.06.23.
//

#ifndef FICTION_WRITE_LOCATION_AND_GROUND_STATE_HPP
#define FICTION_WRITE_LOCATION_AND_GROUND_STATE_HPP

#include "fiction/algorithms/simulation/sidb/exhaustive_ground_state_simulation.hpp"
#include "fiction/algorithms/simulation/sidb/minimum_energy.hpp"
#include "fiction/algorithms/simulation/sidb/sidb_simulation_result.hpp"
#include "fiction/io/read_sqd_layout.hpp"
#include "fiction/technology/charge_distribution_surface.hpp"
#include "fiction/types.hpp"
#include "fiction/utils/math_utils.hpp"

#include <algorithm>
#include <cmath>
#include <fstream>
#include <limits>
#include <ostream>
#include <string>
#include <vector>

namespace fiction
{

namespace detail
{

template <typename Lyt>
class write_location_and_ground_state_impl
{
  public:
    write_location_and_ground_state_impl(const sidb_simulation_result<Lyt>& result, std::ostream& s) :
            sim_result{result},
            os{s}
    {}

    void run()
    {
        // this part searches for the ground state(s) among all physically valid charge distributions
        const auto min_energy =
            round_to_n_decimal_places(minimum_energy<sidb_cell_clk_lyt_siqad>(sim_result.charge_distributions), 6);

        std::vector<charge_distribution_surface<sidb_cell_clk_lyt_siqad>> ground_state_layouts{};
        for (const auto& valid_layout : sim_result.charge_distributions)
        {
            if (std::fabs(round_to_n_decimal_places(valid_layout.get_system_energy(), 6) - min_energy) <
                std::numeric_limits<double>::epsilon())
            {
                ground_state_layouts.emplace_back(charge_distribution_surface<sidb_cell_clk_lyt_siqad>{valid_layout});
            }
        }

        if (!ground_state_layouts.empty())
        {
            // write the column headers
            os << "x [nm]; y [nm];";

            for (uint64_t i = 0; i < ground_state_layouts.size(); i++)
            {
                os << fmt::format("GS_{};", i);
            }
            os << '\n';

            auto       sidbs              = ground_state_layouts.front().get_sidb_order();
            const auto physical_parameter = ground_state_layouts.front().get_phys_params();

            std::sort(sidbs.begin(), sidbs.end());
            for (const auto& sidb : sidbs)
            {
                const auto pos = sidb_nm_position<sidb_cell_clk_lyt_siqad>(physical_parameter, sidb);
                os << fmt::format("{:.3f};{:.3f};", pos.first, pos.second);
                for (const auto& valid_layout : ground_state_layouts)
                {
                    os << fmt::format("{};", charge_state_to_sign(valid_layout.get_charge_state(sidb)));
                }
                os << "\n";
            }
        }
    };

  private:
    /**
     * Simulation results.
     */
    const sidb_simulation_result<Lyt>& sim_result;
    /**
     * Output stream used for writing the simulation result.
     */
    std::ostream& os;
};

}  // namespace detail

/**
 * Writes the coordinates of all SiDBs of a layout together with the charge distribution of the ground state(s) to a
 * file.
 *
 * This overload uses an output stream to write into.
 *
 * @tparam Lyt Cell-level SiDB layout type.
 * @param sim_result The simulation result to write.
 * @param os The output stream to write into.
 */
template <typename Lyt>
void write_location_and_ground_state(const sidb_simulation_result<Lyt>& sim_result, std::ostream& os)
{
    static_assert(is_cell_level_layout_v<Lyt>, "Lyt is not a cell-level layout");
    static_assert(has_sidb_technology_v<Lyt>, "Lyt is not an SiDB layout");
    static_assert(has_siqad_coord_v<Lyt>, "Lyt is not based on SiQAD coordinates");

    detail::write_location_and_ground_state_impl p{sim_result, os};

    p.run();
}

/**
 * Writes the coordinates of all SiDBs of a layout together with the charge distribution of the ground state(s) to a
 * file.
 *
 * This overload uses a file name to create and write into.
 *
 * @tparam Lyt Cell-level SiDB layout type.
 * @tparam sim_result The simulation result to write.
 * @param filename The file name to create and write into.
 */
template <typename Lyt>
void write_location_and_ground_state(const sidb_simulation_result<Lyt>& sim_result, const std::string_view& filename)
{
    std::ofstream os{filename.data(), std::ofstream::out};

    if (!os.is_open())
    {
        throw std::ofstream::failure("could not open file");
    }

    write_location_and_ground_state(sim_result, os);
    os.close();
}

}  // namespace fiction

#endif  // FICTION_WRITE_LOCATION_AND_GROUND_STATE_HPP
