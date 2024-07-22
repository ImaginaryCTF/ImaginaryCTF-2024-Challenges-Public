(*  *)

let width = 65
let height = 65
let maze : bool array array = [| (*MAZE*) |]

let is_position_legal (x, y) =
  maze.(y).(x)

type state = {
  position : int * int
}

type direction = Left | Right | Up | Down

let flag = Bytes.of_string ""(*FLAG*)

let get_key path =
  let hash = Cryptokit.Hash.sha256 () in
  hash#add_string path; hash#result

let decrypt_flag path =
  let key = get_key path in
  let cipher = new Cryptokit.Stream.chacha20 ~iv:"deadbeef" key in
  let buf = Bytes.create (Bytes.length flag) in
  cipher#transform flag 0 buf 0 (Bytes.length buf); String.of_bytes buf 

let update_state { position=(x, y) } dir =
  let new_pos = match dir with
    | Left -> if x > 0 then Some (x - 1, y) else None
    | Right -> if x < width - 1 then Some (x + 1, y) else None
    | Up -> if y > 0 then Some (x, y - 1) else None
    | Down -> if y < height - 1 then Some (x, y + 1) else None
  in
  Option.bind new_pos (fun x -> if is_position_legal x then Some { position=x } else None)

let parse_char c =
  match c with
    | 'L' -> Some Left
    | 'R' -> Some Right
    | 'U' -> Some Up
    | 'D' -> Some Down
    | _ -> None

let () =
  let _ = Printf.printf "As you pick up the scroll, the ground starts shaking! What is the path you'll take to leave the pyramid? %!" in
  let user_input = read_line () in
  let result = String.fold_left (fun os c ->
    let dir = Option.to_result ~none:"You seem to have lost your sense of direction and have no idea what to do." (parse_char c) in
    Result.bind os begin
      fun s -> Result.bind dir begin
        fun d ->
          let new_state = update_state s d in
          Option.to_result ~none:"Wandering through the pyramid, you realise that you don't know where you are. All corridors look exactly the same..." new_state
        end
    end
  ) (Ok { position=(0, 0) }) user_input in
  print_endline begin
    match result with
      | Ok { position=position } -> if position = (width - 1, height - 1) then
          Printf.sprintf "You safely reach the exit and finally have a moment to look at the contents of the scroll you've found: %s" (decrypt_flag user_input)
        else
          "Wandering through the pyramid, you realise that you don't know where you are. All corridors look exactly the same..."
      | Error m -> m
  end