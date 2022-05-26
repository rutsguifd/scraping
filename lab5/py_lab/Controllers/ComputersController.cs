using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using py_lab.Models;
using Microsoft.AspNetCore.Authorization;

namespace py_lab.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ComputersController : ControllerBase
    {

        private readonly PYTHONLABContext _context;

        public ComputersController(PYTHONLABContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<Computer>> GetComputers([FromQuery(Name = "model")] string model)
        {
            var computer = await _context.Computer.FirstOrDefaultAsync(e => e.Model == model);

            if (computer == null)
            {
                return NotFound();
            }

            return computer;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Computer>> GetComputers(int id)
        {
            var computer = await _context.Computer.FindAsync(id);

            if (computer == null)
            {
                return NotFound();
            }

            return computer;
        }

        [HttpPut]
        public async Task<IActionResult> PutComputers(Computer computer)
        {

            var result = await _context.Computer.FirstOrDefaultAsync(b => b.Link == computer.Link);
            if (result != null)
            {
                result.Model = computer.Model;
                result.Price = computer.Price;
                await _context.SaveChangesAsync();
            }
            else
            {
                return BadRequest();
            }

            return NoContent();
        }

        [HttpPost]
        public async Task<ActionResult<Computer>> PostComputers(Computer computer)
        {
            if(_context.Computer.Any(b => b.Model == computer.Model && b.Price == computer.Price && b.Link == computer.Link))
            {
                return Conflict();
            }
            _context.Computer.Add(computer);
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                if (ComputersExists(computer.Id))
                {
                    return Conflict();
                }
                else
                {
                    throw;
                }
            }
            return CreatedAtAction("GetComputers", new { id = computer.Id }, computer);
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult<Computer>> DeleteComputers(int id)
        {
            var computer = await _context.Computer.FindAsync(id);
            if (computer == null)
            {
                return NotFound();
            }

            _context.Computer.Remove(computer);
            await _context.SaveChangesAsync();

            return computer;
        }

        private bool ComputersExists(int id)
        {
            return _context.Computer.Any(e => e.Id == id);
        }
    }
}
